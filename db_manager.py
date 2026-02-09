import sqlite3
from datetime import datetime

DATABASE_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tasks table with complete schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        priority TEXT DEFAULT 'Medium',
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_task(task, date, time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)",
        (task, date, time)
    )
    conn.commit()
    conn.close()

def get_pending_tasks(date, time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task FROM tasks WHERE date=? AND time=? AND status='pending'",
        (date, time)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY date, time ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
