"""Streamlit 主入口 - 系统首页与导航"""

import streamlit as st

st.set_page_config(
    page_title="招聘数据智能系统",
    page_icon="📊",
    layout="wide",
)

st.title("招聘数据智能系统")
st.markdown("基于 NLP 与机器学习的招聘市场数据分析平台")

st.sidebar.success("请从上方导航栏选择功能模块")
