import re
from datetime import datetime, timedelta

def parse_intent(text):
    # find time like 9 or 4
    time_match = re.search(r'\b(\d{1,2})\b', text)

    if not time_match:
        return None

    hour = int(time_match.group(1))

    if "tomorrow" in text:
        date = datetime.now() + timedelta(days=1)
    else:
        date = datetime.now()

    task = text.replace(time_match.group(1), "").strip()

    return {
        "task": task,
        "date": date.strftime("%Y-%m-%d"),
        "time": f"{hour:02d}:00"
    }
    