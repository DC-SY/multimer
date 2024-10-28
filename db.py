import sqlite3
from datetime import datetime

# 连接数据库
conn = sqlite3.connect("data/tasks.db")
cursor = conn.cursor()

# 创建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        start_time DATETIME,
        end_time DATETIME,
        duration INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME,
        deleted_at DATETIME
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_name TEXT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME,
        deleted_at DATETIME
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_tags (
        task_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY (task_id) REFERENCES tasks (task_id),
        FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
    )
""")

conn.commit()


# 示例插入任务
def insert_task(task_name, start_time, end_time):
    duration = int((end_time - start_time).total_seconds() / 60)  # 计算分钟数
    cursor.execute("""
        INSERT INTO tasks (task_name, start_time, end_time, duration)
        VALUES (?, ?, ?, ?)
    """, (task_name, start_time, end_time, duration))
    conn.commit()


# 示例插入标签
def insert_tag(tag_name):
    cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag_name,))
    conn.commit()


# 示例关联任务和标签
def link_task_tag(task_id, tag_id):
    cursor.execute("INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)", (task_id, tag_id))
    conn.commit()


# 插入示例数据
insert_task("完成报告", datetime(2023, 10, 26, 10, 0), datetime(2023, 10, 26, 11, 0))
insert_tag("工作")
link_task_tag(1, 1)

conn.close()
