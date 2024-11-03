import sqlite3

import pandas as pd
import streamlit as st
from components.task_manager import *

# 获取数据
task_data = get_all_tasks()
# 转换为DataFrame
df = pd.DataFrame(task_data, columns=["ID", "任务名称", "开始时间", "结束时间", "持续时间", "创建时间", "更新时间", "删除时间"]).set_index("ID")
# st.dataframe(df.reset_index())
st.dataframe(df)
