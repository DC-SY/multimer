import sqlite3
from datetime import datetime

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 连接数据库
conn = sqlite3.connect("../data/tasks.db")
cursor = conn.cursor()

# 清空所有表
cursor.execute("DROP TABLE IF EXISTS tasks")
cursor.execute("DROP TABLE IF EXISTS tags")
cursor.execute("DROP TABLE IF EXISTS task_tags")

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
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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
# cursor.executemany(""")
cursor.execute("INSERT INTO tags (tag_name, created_at, updated_at) VALUES ('数学', ?, ?)", (current_time, current_time))
cursor.execute("INSERT INTO tags (tag_name, created_at, updated_at) VALUES ('英语', ?, ?)", (current_time, current_time))
cursor.execute("INSERT INTO tags (tag_name, created_at, updated_at) VALUES ('政治', ?, ?)", (current_time, current_time))
cursor.execute("INSERT INTO tags (tag_name, created_at, updated_at) VALUES ('专业课', ?, ?)", (current_time, current_time))
cursor.execute("INSERT INTO tags (tag_name, created_at, updated_at) VALUES ('编程开发', ?, ?)", (current_time, current_time))
conn.commit()
conn.close()
