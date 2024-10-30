import sqlite3

import pandas as pd
import streamlit as st
from components.task_manager import *

# 获取数据
task_data = get_display_tasks()
# 转换为DataFrame
df = pd.DataFrame(task_data, columns=["任务名称", "开始时间", "结束时间", "持续时间", "创建时间"])
st.dataframe(df)
