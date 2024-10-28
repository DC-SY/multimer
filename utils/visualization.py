import matplotlib.pyplot as plt
import streamlit as st

from utils.database import get_connection


def plot_timeline():
    # 使用数据库数据生成时间轴
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task_name, start_time, end_time FROM tasks WHERE deleted_at IS NULL")
        tasks = cursor.fetchall()

    # 绘制时间轴
    st.write("时间轴展示")
    # 实现具体绘图逻辑


def plot_pie_chart():
    # 使用数据库数据生成饼图
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tag_name, COUNT(*) FROM tags JOIN task_tags ON tags.tag_id = task_tags.tag_id GROUP BY tag_name")
        tags = cursor.fetchall()

    labels = [tag[0] for tag in tags]
    sizes = [tag[1] for tag in tags]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)
