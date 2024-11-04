import streamlit as st
import pandas as pd
import time

from components.tag_manager import *
from components.task_manager import *

# Streamlit 页面标题
st.title("多功能任务计时器")

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if 'task_name' not in st.session_state:
    st.session_state.task_name = ""
if 'tags' not in st.session_state:
    st.session_state.tags = None

# 输入框
task_name = st.text_input("请输入任务名称：",placeholder="task name", value=st.session_state.task_name)
# 获取所有标签
all_tags = [tag[0] for tag in get_all_tags_name()]
selected_index = None if st.session_state.tags is None else all_tags.index(st.session_state.tags)

# 选择框
tags = st.selectbox("选择任务标签：", all_tags, index=selected_index, placeholder="tag name")

timer_placeholder = st.empty()

# 开始计时按钮
if st.button("开始任务", disabled=st.session_state.button_clicked):
    if not task_name:
        st.warning("任务名称不能为空！")
    elif not tags:
        st.warning("至少选择一个标签！")
    else:
        start_time = time.time()  # 记录开始时间
        st.session_state.start_time = start_time
        st.session_state.task_name = task_name
        st.session_state.tags = tags
        st.rerun()

# 如果任务已经开始
if 'start_time' in st.session_state:
    st.info("任务已开始！")
    st.session_state.button_clicked = True  # 禁用开始按钮
    # 结束任务按钮
    if st.button('结束任务'):
        if 'start_time' in st.session_state:
            end_time = time.time()
            duration = int(end_time - st.session_state.start_time)
            # duration_formatted = time.strftime("%H:%M:%S", time.gmtime(duration))

            # 保存任务信息到数据库
            new_task = {
                "任务名称": st.session_state.task_name,
                "任务标签": st.session_state.tags,
                "开始时间": pd.Timestamp(st.session_state.start_time, unit='s'),
                "结束时间": pd.Timestamp(end_time, unit='s'),
                "持续时间": duration
            }
            add_task(new_task)

            # 清空计时器
            timer_placeholder.empty()
            st.balloons()
            st.success(f"任务 '{st.session_state.task_name}' 已结束！持续时间: {duration}秒", icon="✅")
            st.session_state.button_clicked = False  # 启用开始按钮
            # 清除 start_time 以结束计时器循环
            del st.session_state.start_time
            # time.sleep(3)
            # st.rerun()

    # 动态更新计时器
    while 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time  # 计算任务已经进行的时间
        elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # 格式化时间
        # 更新页面上的计时器显示
        timer_placeholder.markdown(f"### 当前任务已进行时间: {elapsed_time_formatted}")
        # 每秒刷新一次
        time.sleep(1)
