from datetime import datetime

import streamlit as st
import pandas as pd
import time
import sqlite3

from annotated_text import annotation, annotated_text
from streamlit_tags import st_tags

# 设置页面配置为全屏显示
st.set_page_config(layout="wide")

# 初始化 session state 数据
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["date", "weekday", "task_name", "tag", "time_used"])
if "current_task" not in st.session_state:
    st.session_state.current_task = None
if "tags" not in st.session_state:
    st.session_state.tags = ["专业课", "英语", "数学", "政治"]

# 左中右布局
left_col, center_col, right_col = st.columns([1, 2, 1])

# 时间变量
today = pd.Timestamp.today().date()
this_week = today - pd.Timedelta(days=today.weekday())

# 左侧：今天和本周已完成任务
with left_col:
    st.header("任务统计")
    st.markdown('---')
    # 今日已完成任务
    st.subheader("今天已完成的任务")
    today_tasks = st.session_state.tasks[st.session_state.tasks['date'] == today]

    if not today_tasks.empty:
        today_tasks = today_tasks.reset_index().rename(columns={'index': '序号'})
        st.table(today_tasks[['序号', 'task_name', 'time_used']])
    else:
        annotated_text(
            annotation("请创建任务", font_family="Comic Sans MS", border="2px dashed red"),
        )

    # 本周已完成任务
    st.subheader("本周完成的任务")
    week_tasks = st.session_state.tasks[st.session_state.tasks['date'] >= this_week]

    if not week_tasks.empty:
        week_tasks = week_tasks.reset_index().rename(columns={'index': '序号'})
        st.table(week_tasks[['weekday', '序号', 'task_name', 'time_used']])
    else:
        annotated_text(
            annotation("请创建任务", font_family="Comic Sans MS", border="2px dashed red"),
        )
# 中间：任务计时和管理
with center_col:
    st.header("多功能任务计时器")
    st.markdown('---')
    task_name = st.text_input("输入任务名")
    # tag = st.selectbox("选择任务标签", options=st.session_state.tags + ["创建新标签"])

    # # 标签管理
    # if tag == "创建新标签":
    #     new_tag = st.text_input("请输入新标签名称")
    #     if st.button("添加标签"):
    #         if new_tag not in st.session_state.tags:
    #             st.session_state.tags.append(new_tag)
    #             st.success(f"标签 {new_tag} 已添加")

    # # 开始任务
    # if st.button("开始任务") and task_name:
    #     st.session_state.current_task = {
    #         "task_name": task_name,
    #         "tag": tag,
    #         "start_time": time.time()
    #     }
    #     st.info("任务已开始")

    # 显示任务计时和结束按钮
    if st.session_state.current_task:
        elapsed_time = time.time() - st.session_state.current_task["start_time"]
        st.write(f"任务进行中：{st.session_state.current_task['task_name']} - 已用时：{elapsed_time:.2f} 秒")

        if st.button("结束任务"):
            # 记录完成的任务
            end_time = time.time()
            time_used = end_time - st.session_state.current_task["start_time"]
            task_data = {
                "date": today,
                "weekday": today.strftime("%A"),
                "task_name": st.session_state.current_task["task_name"],
                "tag": st.session_state.current_task["tag"],
                "time_used": f"{time_used / 60:.2f} 分钟"
            }
            st.session_state.tasks = st.session_state.tasks.append(task_data, ignore_index=True)
            st.success(f"任务 {st.session_state.current_task['task_name']} 已完成，用时 {task_data['time_used']}")
            st.session_state.current_task = None

# 右侧：今日任务列表和任务标签
with right_col:
    st.header("任务和标签管理")
    st.markdown('---')
    # st.subheader("今日任务列表")
    # today_tasks_created = st.session_state.tasks[st.session_state.tasks['date'] == today][['task_name']]
    # st.write(today_tasks_created)
    #
    # keywords = st_tags(
    #     label='### 任务标签：',
    #     text='Press enter to add more',
    #     value=st.session_state.tags,
    #     suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],
    #
    #     maxtags=4,
    #     key='1')
    # 连接到SQLite数据库
    def get_db_connection():
        conn = sqlite3.connect('tasks.db')  # 替换为你的数据库文件路径
        conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
        return conn


    # 初始化数据库（若表不存在则创建）
    def init_db():
        conn = get_db_connection()
        cursor = conn.cursor()

        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                deleted_at DATETIME
            )
        """)
        conn.commit()
        conn.close()

    # 获取所有标签
    def get_all_tags():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tags WHERE deleted_at IS NULL")
        tags_ = cursor.fetchall()
        conn.close()
        return tags_

    # 添加新标签
    def add_tag(tag_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag_name,))
        conn.commit()
        conn.close()

    # 删除标签（软删除，更新deleted_at字段）
    def delete_tag(tag_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tags SET deleted_at = ? WHERE tag_id = ?", (datetime.now(), tag_id))
        conn.commit()
        conn.close()

    # 初始化数据库
    init_db()

    # 显示标签
    st.header("现有标签")
    tags = get_all_tags()
    for tag in tags:
        col1, col2 = st.columns([3, 1])
        col1.write(tag["tag_name"])
        if col2.button("删除", key=tag["tag_id"]):
            delete_tag(tag["tag_id"])
            st.success("标签已删除")
            time.sleep(1)
            # st.experimental_rerun()  # 重新加载页面以刷新标签列表
            st.rerun()  # 重新加载页面以刷新标签列表

    # 添加新标签
    st.header("添加新标签")
    # new_tag = st.text_input("标签名称")
    # 使用 session state 来存储输入框的内容
    if "input_value" not in st.session_state:
        st.session_state.input_value = ""


    def clear_input():
        # 清空输入框内容
        st.session_state.input_value = ""

    # 创建输入框，绑定到 session state
    new_tag = st.text_input("标签名称", key="input_value", on_change=clear_input)
    if st.button("添加标签"):
        if new_tag:
            try:
                add_tag(new_tag)
                st.success("标签添加成功！")
                time.sleep(1)
                st.rerun()  # 重新加载页面以刷新标签列表
            except sqlite3.IntegrityError:
                st.error("标签已存在！")
        else:
            st.warning("请输入标签名称")