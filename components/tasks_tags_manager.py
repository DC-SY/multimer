from components.task_manager import *
from components.tag_manager import *


def add_task_tag(task_name_: str, tag_name_: str):
    # 获取任务id
    task_id = get_task_id(task_name_)
    # 获取标签id
    tag_id = get_tag_id(tag_name_)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)", (task_id, tag_id))
        conn.commit()
