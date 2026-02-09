import dateparser
from dateparser.search import search_dates
from intent_parser import normalize_vocal_time, parse_all_tasks
from datetime import datetime

def debug_failure(text):
    print(f"INPUT: {text}")
    print(f"NOW:   {datetime.now()}")
    
    norm = normalize_vocal_time(text)
    print(f"NORM:  {norm}")
    
    found = search_dates(norm, settings={'PREFER_DATES_FROM': 'future'})
    print(f"FOUND ANCHORS: {found}")
    
    results = parse_all_tasks(text)
    print(f"RESULTS: {results}")

if __name__ == "__main__":
    debug_failure("set a reminder to check email the day after today at 3:00 a.m.")
