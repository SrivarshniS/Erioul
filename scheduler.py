import time
from datetime import datetime
from speaker import speak
import db_manager

def check_reminders():
    """Background loop to check for pending tasks and speak reminders."""
    while True:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        tasks = db_manager.get_pending_tasks(current_date, current_time)

        for task_id, task_text in tasks:
            speak(f"Reminder. It's time for {task_text}")
            db_manager.update_task_status(task_id, 'done')

        time.sleep(30)
