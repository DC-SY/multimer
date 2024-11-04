import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from components.task_manager import *

tab1, tab2, tab3 = st.tabs(["展示任务记录", "任务表格交互", "任务-CRUD"])

with tab1:
    # 获取数据
    task_data = get_all_tasks()
    # 转换为DataFrame
    df = pd.DataFrame(task_data,
                      columns=["序号", "任务名称", "开始时间", "结束时间", "持续时间", "创建时间", "更新时间",
                               "删除时间"]).set_index("序号")
    st.dataframe(df, width=1000, height=600)
with tab2:
    df = pd.DataFrame(task_data,
                      columns=["序号", "任务名称", "开始时间", "结束时间", "持续时间", "创建时间", "更新时间",
                               "删除时间"]).set_index("序号")
    # st.dataframe(df.reset_index())
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True, sortable=True)
    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        height=600,
        width='100%',
        # theme='light',
    )
    st.write("这是第二个标签页: 与任务交互")
