import pandas as pd

from utils.database import get_connection


def add_task(new_task_: dict):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task_name, start_time, end_time, duration, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (new_task_["任务名称"], new_task_["开始时间"].strftime("%Y-%m-%d %H:%M:%S"),
             new_task_["结束时间"].strftime("%Y-%m-%d %H:%M:%S"), new_task_["持续时间"],
             pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()


def get_display_tasks():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT task_name, start_time, end_time, duration, created_at FROM tasks WHERE deleted_at IS NULL")
        return cursor.fetchall()


def get_all_tasks():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()


# 可扩展其他函数：update_task, delete_task等
def get_task_id(task_name_: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task_id FROM tasks WHERE task_name = ?", (task_name_,))
        return cursor.fetchone()[0]


