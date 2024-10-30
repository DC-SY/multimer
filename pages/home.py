import streamlit as st
import pandas as pd
import time
import os

# 文件名
filename = 'tasks.xlsx'

# 全局变量初始化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []  # 存储当前页面创建的任务

# Streamlit 页面标题
st.title("任务计时器")

# 获取任务名称和标签
task_name = st.text_input("请输入任务名称：")
tags = st.multiselect("选择任务标签：", ["专业课", "英语", "数学", "政治"])

# 初始化计时器占位符
timer_placeholder = st.empty()

# 开始计时按钮
if st.button("开始任务"):
    if not task_name:
        st.warning("任务名称不能为空！")
    elif not tags:
        st.warning("至少选择一个标签！")
    else:
        start_time = time.time()  # 记录开始时间
        st.session_state.start_time = start_time
        st.session_state.task_name = task_name
        st.session_state.tags = tags
        st.success(f"任务 '{task_name}' 已开始！")

        # 动态更新计时器
        while 'start_time' in st.session_state:
            elapsed_time = time.time() - st.session_state.start_time  # 计算任务已经进行的时间
            elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # 格式化时间

            # 更新页面上的计时器显示
            timer_placeholder.markdown(f"### 当前任务已进行时间: {elapsed_time_formatted}")

            # 每秒刷新一次
            time.sleep(1)

# 结束任务按钮
if st.button("结束任务") and 'start_time' in st.session_state:
    end_time = time.time()  # 记录结束时间
    duration = end_time - st.session_state.start_time  # 计算任务持续时间（秒）
    duration_formatted = time.strftime("%H:%M:%S", time.gmtime(duration))  # 格式化时间为时分秒

    # 保存任务信息到字典
    new_task = {
        "任务名称": st.session_state.task_name,
        "标签": ", ".join(st.session_state.tags),
        "开始时间": pd.Timestamp(st.session_state.start_time, unit='s'),
        "结束时间": pd.Timestamp(end_time, unit='s'),
        "持续时间": duration_formatted
    }

    # 添加到任务列表
    st.session_state.tasks.append(new_task)

    # # 将任务保存到 Excel 文件
    # df = pd.DataFrame(st.session_state.tasks)
    #
    # if os.path.exists(filename):
    #     # 如果文件存在，读取现有数据并追加新任务
    #     existing_df = pd.read_excel(filename)
    #     df = pd.concat([existing_df, df], ignore_index=True)
    #
    # # 将合并后的数据保存回 Excel 文件
    # df.to_excel(filename, index=False)

    # 清空计时器
    timer_placeholder.empty()

    st.success(f"任务 '{st.session_state.task_name}' 已结束！持续时间: {duration_formatted}")

    # 清除 start_time 以结束计时器循环
    del st.session_state.start_time

# 显示已经完成的任务
if os.path.exists(filename):
    st.subheader("已完成的任务记录")
    df = pd.read_excel(filename)
    st.dataframe(df)
#
# # 任务统计报表
# if st.button("生成报表"):
#     if os.path.exists(filename):
#         df = pd.read_excel(filename)
#         df['日期'] = pd.to_datetime(df['开始时间']).dt.date
#
#         # 日报表
#         daily_report = df.groupby('日期').agg({'持续时间': 'sum'}).reset_index()
#         st.subheader("日报表")
#         st.dataframe(daily_report)
#
#         # 周报表
#         df['周'] = pd.to_datetime(df['开始时间']).dt.isocalendar().week
#         weekly_report = df.groupby('周').agg({'持续时间': 'sum'}).reset_index()
#         st.subheader("周报表")
#         st.dataframe(weekly_report)
#
#         # 月报表
#         df['月份'] = pd.to_datetime(df['开始时间']).dt.to_period('M')
#         monthly_report = df.groupby('月份').agg({'持续时间': 'sum'}).reset_index()
#         st.subheader("月报表")
#         st.dataframe(monthly_report)
#     else:
#         """
#         奇技淫巧
#         """
#         st.warning("没有任务记录，无法生成报表！")
