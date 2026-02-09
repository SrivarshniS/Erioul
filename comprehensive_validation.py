from intent_parser import parse_all_tasks
from datetime import datetime

def run_test(name, text, f):
    f.write(f"\n>>> TEST: {name}\n")
    f.write(f"Input:  {text}\n")
    results = parse_all_tasks(text)
    if not results:
        f.write("  RESULT: NO TASKS FOUND\n")
    for i, (task, date, time) in enumerate(results):
        f.write(f"  RESULT {i+1}: Task='{task}' | Date={date} | Time={time}\n")

def main():
    test_cases = [
        ("Identified Bug", "breakfast at 9:00 a.m. and dinner at 10:00 p.m."),
        ("Multi-Task with Connectors", "buy milk at 5 then call mom at 6 also gym at 7"),
        ("Relative Date Combinations", "the day before tomorrow afternoon yoga session and day after today morning standup"),
        ("Military Time Cleanup", "1530 coffee meeting and 0900 gym"),
        ("Redundant Words", "morning 9:00 standup at the office on Monday"),
        ("Ultimate Stress Test", "Tomorrow morning at 9:30 I have a project review, then at 11:15 call the supplier about the delayed shipment, after that set a reminder to prepare slides for next week, and by 6 PM check emails and respond to urgent ones, but skip the yoga session I usually do in the evening."),
        ("Negation & Action Words", "remind me to go to the gym at 8:00 but don't set a reminder for breakfast at 9:00"),
        ("Ambiguous Relative", "set a task to check email the day after today at 3:00")
    ]
    
    with open('final_precision_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"System Time: {datetime.now()}\n")
        for name, text in test_cases:
            run_test(name, text, f)

if __name__ == "__main__":
    main()
