import time
import sqlite3
from utils.database import get_connection

def start_timer(task_id):
    start_time = time.time()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET start_time = ? WHERE task_id = ?", (start_time, task_id))
        conn.commit()

def stop_timer(task_id):
    end_time = time.time()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET end_time = ?, duration = ? WHERE task_id = ?",
                       (end_time, end_time - start_time, task_id))
        conn.commit()
