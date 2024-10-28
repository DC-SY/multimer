import streamlit as st
from utils.visualization import plot_timeline, plot_pie_chart

def show():
    st.title("数据可视化分析")
    plot_timeline()
    plot_pie_chart()
