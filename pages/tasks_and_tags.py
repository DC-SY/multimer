import streamlit as st
from components.tasks_tags_manager import *

tab1, tab2 = st.tabs(["展示任务-标签", "展示标签-任务"])

with tab1:
    pass
    data = get_all_task_tags()
    df = pd.DataFrame(data, columns=["任务名称", "创建时间", "持续时间/s", "标签名称"], index=None)
    st.dataframe(df)
with tab2:
    pass
