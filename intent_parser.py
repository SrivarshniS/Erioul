import dateparser
import re
from datetime import datetime
from dateparser.search import search_dates

def normalize_vocal_time(text):
    """
    Normalizes vocal time patterns like '930' to '9:30 ' 
    and 'at 9' to 'at 9:00' to help dateparser.
    """
    # 1. 'at 9' -> 'at 9:00'
    text = re.sub(r'\bat\s+(\d{1,2})\b(?!\s*[:\d])', r'at \1:00', text, flags=re.IGNORECASE)
    
    # 2. Military time/Colon-less time like '930' or '1530'
    # Added a space after the replacement to prevent concatenation with next word
    text = re.sub(r'\b(\d{1,2})(\d{2})\b', 
                  lambda m: f"{m.group(1)}:{m.group(2)} ", 
                  text, flags=re.IGNORECASE)
    
    # 3. Handle 'am/pm' spacing issues if military regex created '15:30am'
    text = re.sub(r'(\d):(?=\d{2}(am|pm|a\.m|p\.m))', r'\1:', text, flags=re.IGNORECASE)
    
    # 4. Relative Date Normalization (Flexible 'the')
    text = re.sub(r'\b(?:the\s+)?day\s+before\s+today\b', 'yesterday', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(?:the\s+)?day\s+before\s+tomorrow\b', 'today', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(?:the\s+)?day\s+after\s+today\b', 'tomorrow', text, flags=re.IGNORECASE)
    
    # 5. Time-of-Day Normalization - ONLY if NOT followed by a specific time or 'at'
    text = re.sub(r'\bmorning\b(?!\s*(?:at\s+)?(?:\d|am|pm))', 'at 8:00', text, flags=re.IGNORECASE)
    text = re.sub(r'\bforenoon\b(?!\s*(?:at\s+)?(?:\d|am|pm))', 'at 11:00', text, flags=re.IGNORECASE)
    text = re.sub(r'\bafternoon\b(?!\s*(?:at\s+)?(?:\d|am|pm))', 'at 13:00', text, flags=re.IGNORECASE)
    text = re.sub(r'\bevening\b(?!\s*(?:at\s+)?(?:\d|am|pm))', 'at 18:00', text, flags=re.IGNORECASE)
    text = re.sub(r'\bnight\b(?!\s*(?:at\s+)?(?:\d|am|pm))', 'at 21:00', text, flags=re.IGNORECASE)

    # Cleanup any "at at" or duplicate symbols
    text = re.sub(r'\bat\s+at\b', 'at', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_task_time(text):
    """
    Legacy wrapper for extracting task/time from a single segment.
    """
    results = parse_all_tasks(text)
    if results:
        return results[0] # Return the first one found
    return text, None, None

def parse_all_tasks(text):
    """
    Unified parsing pipeline.
    Finds all tasks and times in a single pass using search_dates anchors.
    """
    # 1. Pre-normalize
    text = normalize_vocal_time(text)
    
    # 2. Find internal time anchors
    found = search_dates(text, settings={'PREFER_DATES_FROM': 'future'})
    
    if not found:
        return []

    # 3. Identify spans and merge close anchors
    raw_spans = []
    last_search_pos = 0
    for phrase, dt in found:
        idx = text.find(phrase, last_search_pos)
        if idx != -1:
            raw_spans.append({"start": idx, "end": idx + len(phrase), "dt": dt, "phrase": phrase})
            last_search_pos = idx + len(phrase)
    
    if not raw_spans:
        return []

    # Merge logic
    merged = []
    if raw_spans:
        curr = raw_spans[0]
        for i in range(1, len(raw_spans)):
            nxt = raw_spans[i]
            gap = text[curr["end"]:nxt["start"]].strip().lower()
            # Merge if gap is small or relative indicators
            if not gap or gap in ["at", "on", "in", "for", "by", "today", "tomorrow", "yesterday", "morning", "evening", "night", "forenoon", "afternoon", "the"]:
                curr["end"] = nxt["end"]
                curr["phrase"] = text[curr["start"]:curr["end"]]
                
                # PREFERENCE LOGIC: 
                # If nxt has a time component (detected by having a colon or 'am/pm'), it's more specific.
                # dateparser's dt object usually has the time 00:00 if it's just a date.
                # However, HH:MM is what the user said.
                curr["dt"] = nxt["dt"]
            else:
                merged.append(curr)
                curr = nxt
        merged.append(curr)

    # 4. Associate text with anchors using connector-based splitting
    task_parts = [[] for _ in range(len(merged))]
    
    # Prefix for the first anchor
    task_parts[0].append(text[0:merged[0]["start"]])
    
    # Parts between anchors
    for i in range(len(merged) - 1):
        gap = text[merged[i]["end"]:merged[i+1]["start"]]
        # Split gap by common task connectors, punctuation, or 'but' for negation segments
        # We split but KEEP the negation words to detect them in the next step
        parts = re.split(r'\s+(?:and|then|also|after that|afterwards|next|but)\s+|,\s+', gap, flags=re.IGNORECASE)
        
        # The first part belongs to the current anchor (as a suffix)
        task_parts[i].append(parts[0])
        # All subsequent parts belong to the next anchor (as a prefix)
        for p in parts[1:]:
            task_parts[i+1].append(p)
            
    # Suffix for the last anchor
    task_parts[-1].append(text[merged[-1]["end"]:])
    
    # 5. Clean up and finalize
    results = []
    noise_words = {"today", "tomorrow", "yesterday", "morning", "evening", "night", "forenoon", "afternoon", "at", "on", "the", "day", "before", "after", "am", "pm", "a.m", "p.m", "by", "for", "this", "that", "i", "a", "an", "the", "week", "month", "next"}
    negation_words = {"skip", "cancel", "don't", "do not", "nevermind", "ignore", "remove"}
    
    for i, anchor in enumerate(merged):
        raw_task = " ".join(task_parts[i])
        
        # NEGATION DETECTION: Skip if this segment implies cancellation
        if any(neg in raw_task.lower() for neg in negation_words):
            continue

        # Word-level cleanup
        words = raw_task.split()
        cleaned_words = [w for w in words if w.lower().strip(",.") not in noise_words]
        task = " ".join(cleaned_words)

        # Prefix/Suffix cleanup - remove common vocal filler patterns
        while True:
            # Prefix cleanup
            new_task = re.sub(r'^(and|then|also|after that|afterwards|next|do|go to|remind me to|remember to|set a task to|set reminder for|set a reminder to|set reminder to|i have a|i have an|check|respond to|prepare|prepare for|start|set a reminder|set task to|have|has|had)\s+', '', task, flags=re.IGNORECASE)
            # Suffix cleanup
            new_task = re.sub(r'\s+(in|for|and|then|also|about|next|week|month|session|due|as well)$', '', new_task, flags=re.IGNORECASE)
            
            if new_task == task:
                break
            task = new_task
            
        task = re.sub(r'\s+', ' ', task).strip(",. ")
        
        if task:
            # Final check to see if the anchor phrase itself should be removed if it leaked
            # Though association logic usually prevents this.
            date_str = anchor["dt"].strftime("%Y-%m-%d")
            time_str = anchor["dt"].strftime("%H:%M")
            results.append((task, date_str, time_str))

    return results

def identify_intent(text):
    """
    Identifies the user's intent with more robust keyword matching.
    Returns: 'list', 'delete', 'add', 'help', 'cancel'
    """
    text = text.lower().strip()
    
    # Precise command matches first
    if any(word in text for word in ["list", "show", "what", "my tasks", "reminders", "agenda", "schedule"]):
        return "list"
    if any(word in text for word in ["delete", "remove", "clear", "cancel my task", "bin", "trash"]):
        # Special check: if they just say "cancel", it's a general cancel
        if text == "cancel" or text == "stop" or text == "nevermind":
            return "cancel"
        return "delete"
    if any(word in text for word in ["help", "what can you do", "commands", "instructions"]):
        return "help"
    if any(word in text for word in ["stop", "cancel", "exit", "quit", "goodbye"]):
        return "cancel"

    # Default to 'add' if there's any content, otherwise None
    return "add" if len(text) > 0 else None

def extract_task_id(text):
    """Extracts a numeric ID from text for deletion, handling common phrasing."""
    # Matches "delete number 5", "remove 5", "task 5", etc.
    match = re.search(r'\b(?:task|number|id|#)?\s*(\d+)\b', text, re.IGNORECASE)
    return int(match.group(1)) if match else None
