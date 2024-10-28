import sqlite3
from utils.database import get_connection

def add_task(task_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
        conn.commit()

def get_tasks():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE deleted_at IS NULL")
        return cursor.fetchall()

# 可扩展其他函数：update_task, delete_task等
