import streamlit as st
from altair.vega import autosize
from st_aggrid import AgGrid, GridOptionsBuilder

from components.tag_manager import get_all_tags
from components.task_manager import *

tab1, tab2, tab3 = st.tabs(["展示标签记录", "标签表格交互", "标签-CRUD"])

with tab1:
    # 获取数据
    task_data = get_all_tags()
    # 转换为DataFrame
    df = pd.DataFrame(task_data,
                      columns=["序号", "标签名称", "创建时间", "更新时间", "删除时间"]).set_index("序号")
    st.dataframe(df, width=1000, height=None)
    height = 600
with tab2:
    df = pd.DataFrame(task_data,
                      columns=["序号", "标签名称", "创建时间", "更新时间", "删除时间"]).set_index("序号")
    # st.dataframe(df.reset_index())
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True, sortable=True)
    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        height=300,
        width='100%',
        domLayout='autoHeight',
        fit_columns_on_grid_load=True,
    )
with tab3:
    st.header("这是第二个标签页: 标签-CRUD")
    st.markdown("""
    > 扩展功能：任务的增删改查
    1. 可以先添加任务，而不进行任务
    2. 可以删除任务，支持软删除
    3. 可以更新任务，支持更新任务名称、开始时间、结束时间、持续时间
    """)
