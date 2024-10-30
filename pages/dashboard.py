import streamlit as st
from streamlit import session_state

from utils.visualization import plot_timeline, plot_pie_chart

def show():
    st.title("数据可视化分析")
    plot_timeline()
    plot_pie_chart()

# 初始化按钮状态
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False
# 使用 session_state 记录计数
if 'count_' not in st.session_state:
    st.session_state.count_ = 0
# 当按钮点击后将其禁用
if st.button("点击后禁用按钮", disabled=st.session_state.button_disabled) and not st.session_state.button_disabled:
    st.write("按钮已点击，执行操作...")
    st.write("操作完成！")
    session_state.count_ += 1
    st.write(f"按钮点击次数：{st.session_state.count_}")
    st.session_state.button_disabled = True  # 点击后禁用按钮

