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


conn.close()
