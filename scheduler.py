import sqlite3
from datetime import datetime
from speaker import speak
import time

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    date TEXT,
    time TEXT,
    status TEXT
)
""")
conn.commit()


def add_task(task, date, time_):
    cursor.execute(
        "INSERT INTO tasks (task, date, time, status) VALUES (?, ?, ?, ?)",
        (task, date, time_, "pending")
    )
    conn.commit()


def check_reminders():
    while True:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        cursor.execute("""
            SELECT id, task FROM tasks
            WHERE date=? AND time=? AND status='pending'
        """, (current_date, current_time))

        tasks = cursor.fetchall()

        for task in tasks:
            speak(f"Reminder. It's time for {task[1]}")
            cursor.execute(
                "UPDATE tasks SET status='done' WHERE id=?",
                (task[0],)
            )
            conn.commit()

        time.sleep(30)
