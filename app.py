import streamlit as st
from pages import dashboard, task_page, tag_page

# 设置页面配置
st.set_page_config(page_title="多功能计时器", layout="wide", initial_sidebar_state="expanded")

# 美化侧边栏标题和说明
st.sidebar.title("多功能计时器")
st.sidebar.markdown("🔹 一个用于任务管理的多功能计时器")

# 创建侧边栏导航选项
menu_options = ["主页", "任务管理", "标签管理", "数据可视化"]
selected_page = st.sidebar.radio("导航菜单", menu_options)

# 根据选项显示不同页面内容
if selected_page == "主页":
    st.title("欢迎使用多功能计时器")
    st.write("请选择左侧菜单来访问不同功能页面。")
    # st.image("assets/timer_image.png")  # 可选择放置一张介绍图片
elif selected_page == "任务管理":
    task_page.show()  # 加载任务管理页面
elif selected_page == "标签管理":
    tag_page.show()  # 加载标签管理页面
elif selected_page == "数据可视化":
    dashboard.show()  # 加载数据可视化页面
