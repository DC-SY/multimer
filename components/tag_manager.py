import sqlite3
from datetime import datetime

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
def get_all_tags_name():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tag_name FROM tags WHERE deleted_at IS NULL")
        return cursor.fetchall()

def get_all_tags():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tags")
        rows = cursor.fetchall()
        # Convert timestamps to dates
        result = []
        for row in rows:
            row = list(row)
            for i in [2, 3, 4]:  # Assuming created_at, updated_at, deleted_at are at index 2, 3, 4
                if row[i]:
                    row[i] = str(datetime.fromtimestamp(int(row[i]) / 1000).date())
                    # row[i] = datetime.strptime(str(int(row[i]/1000)), '%Y-%m-%d %H:%M:%S').date()
            result.append(tuple(row))
        return result
        # return cursor.fetchall()

def get_tag_id(tag_name_: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag_name_,))
        return cursor.fetchone()[0]
