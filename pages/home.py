import streamlit as st
import pandas as pd
import time

from components.tag_manager import get_all_tags

# Streamlit 页面标题
st.title("任务计时器")

# 全局变量初始化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []  # 存储当前页面创建的任务
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# 获取任务名称
task_name = st.text_input("请输入任务名称：")

# 选择数据库中存储的标签
tags = st.multiselect("选择任务标签：", [tag[0] for tag in get_all_tags()])

# 定义计时器
# 初始化计时器占位符
timer_placeholder = st.empty()

if 'start_time' in st.session_state:
    st.write("任务已开始！")
    st.session_state.button_clicked = True  # 禁用开始按钮
    # 结束任务按钮
    if st.button('结束任务', key=1):
        if 'start_time' in st.session_state:
            end_time = time.time()
            duration = end_time - st.session_state.start_time
            duration_formatted = time.strftime("%H:%M:%S", time.gmtime(duration))

            # 保存任务信息到字典
            new_task = {
                "任务名称": st.session_state.task_name,
                "任务标签": ", ".join(st.session_state.tags),
                "开始时间": pd.Timestamp(st.session_state.start_time, unit='s'),
                "结束时间": pd.Timestamp(end_time, unit='s'),
                "持续时间": duration_formatted
            }

            # 添加到任务列表
            st.session_state.tasks.append(new_task)

            # 显示已完成的任务
            st.subheader("已完成的任务")
            st.dataframe(pd.DataFrame(st.session_state.tasks))

            # 清空计时器
            timer_placeholder.empty()

            st.success(f"任务 '{st.session_state.task_name}' 已结束！持续时间: {duration_formatted}")
            st.session_state.button_clicked = False  # 启用开始按钮
            # 清除 start_time 以结束计时器循环
            del st.session_state.start_time

    # 动态更新计时器
    while 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time  # 计算任务已经进行的时间
        elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # 格式化时间

        # 更新页面上的计时器显示
        timer_placeholder.markdown(f"### 当前任务已进行时间: {elapsed_time_formatted}")

        # 每秒刷新一次
        time.sleep(1)

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
        # st.success(f"任务 '{task_name}' 已开始！")
