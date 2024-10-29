import streamlit as st

pages = {
    "主页": [
        st.Page("pages/home.py", title="主页"),
    ],
    "任务管理": [
        st.Page("pages/task_page.py", title="任务管理"),
    ],
    "标签管理": [
        st.Page("pages/tag_page.py", title="标签管理"),
    ],
    "数据可视化": [
        st.Page("pages/dashboard.py", title="数据可视化"),
    ],
}
pg = st.navigation(pages)
pg.run()
