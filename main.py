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

    # 开始任务
    if st.button("开始任务") and task_name:
        st.session_state.current_task = {
            "task_name": task_name,
            "tag": tag,
            "start_time": time.time()
        }
        st.info("任务已开始")

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
    st.subheader("今日任务列表")
    today_tasks_created = st.session_state.tasks[st.session_state.tasks['date'] == today][['task_name']]
    st.write(today_tasks_created)

    keywords = st_tags(
        label='### 任务标签：',
        text='Press enter to add more',
        value=st.session_state.tags,
        suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],

        maxtags=4,
        key='1')
