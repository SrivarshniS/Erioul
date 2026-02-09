import threading
from datetime import datetime
from listener import listen
from speaker import speak
from intent_parser import identify_intent, extract_task_id, parse_all_tasks, extract_task_time
import db_manager
from scheduler import check_reminders

def main():
    # Initialize database with unified schema
    db_manager.initialize_db()

    # Start scheduler in background thread
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

    speak("Hello, I am Erioul. Task organizer ready.")

    while True:
        input("Press ENTER to talk...\n")

        speak("I'm listening")
        text = listen()

        if not text:
            # speak("I didn't hear anything.")
            continue

        intent = identify_intent(text)

        if intent == "help":
            speak("I can help you manage your tasks. You can say 'Add buy milk at 5pm', 'Show my tasks' to see the list, or 'Delete task 1' to remove one.")
            continue

        elif intent == "cancel":
            speak("Cancelled.")
            continue

        elif intent == "list":
            tasks = db_manager.get_all_tasks()
            if not tasks:
                speak("Your task list is empty.")
            else:
                speak("Here are your tasks:")
                for t in tasks:
                    # t format: (id, task, date, time, ...)
                    date_display = t[2] if t[2] else "Unscheduled date"
                    time_display = t[3] if t[3] else "Unscheduled time"
                    speak(f"ID {t[0]}: {t[1]} on {date_display} at {time_display}")

        elif intent == "delete":
            task_id = extract_task_id(text)
            if task_id:
                speak(f"Are you sure you want to delete task {task_id}?")
                conf = listen()
                if conf and any(word in conf.lower() for word in ["yes", "yeah", "sure", "can", "ok"]):
                    db_manager.delete_task(task_id)
                    speak(f"Task {task_id} deleted.")
                else:
                    speak("Deletion cancelled.")
            else:
                speak("I couldn't find a task ID to delete. Please say the ID number.")

        elif intent == "add":
            tasks_to_save = parse_all_tasks(text)

            if not tasks_to_save:
                # Fallback: if no time found, try to extract just a task and ask for time
                task, _, _ = extract_task_time(text)
                if task:
                    speak(f"When should I remind you to {task}?")
                    time_reply = listen()
                    if time_reply:
                        _, date_str, time_str = extract_task_time("at " + time_reply)
                        if date_str and time_str:
                            tasks_to_save = [(task, date_str, time_str)]

            if not tasks_to_save:
                speak("I couldn't clarify the task details. Please say the task and the time.")
                continue

            # STEP 3 — confirmation sentence
            summary = " and ".join(
                [f"{task} at {time_str}" for task, date_str, time_str in tasks_to_save]
            )

            speak(f"You have {summary}. Should I save these?")
            confirmation = listen()
            
            if confirmation:
                confirmation = confirmation.lower().strip()
                print(f"DEBUG: confirmation received: '{confirmation}'")

            if confirmation and any(word in confirmation for word in ["yes", "yeah", "sure", "can", "save", "ok"]):
                for task, date_str, time_str in tasks_to_save:
                    db_manager.save_task(task, date_str, time_str)
                speak("Tasks saved and scheduled.")
            else:
                speak("Okay, not saved.")
        
        else:
            speak("I'm not sure what you mean. You can say 'help' for examples.")

if __name__ == "__main__":
    main()
