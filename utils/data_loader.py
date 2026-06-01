import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/real_madrid.csv")
