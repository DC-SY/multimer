import sqlite3
from utils.database import get_connection

def add_tag(tag_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag_name,))
        conn.commit()

def get_display_tags():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tags WHERE deleted_at IS NULL")
        return cursor.fetchall()

# 可扩展其他函数：update_tag, delete_tag等
