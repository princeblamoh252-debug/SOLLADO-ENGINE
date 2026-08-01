import streamlit as st
import random

st.set_page_config(page_title="SOLLADO ENGINE v6.0", layout="wide")

st.title("⚡ SOLLADO ENGINE v6.0")
st.subheader("Stronger, Secure, No-Crash Football Predictor")
st.divider()

st.header("Step 1: Enter Teams")
col1, col2 = st.columns(2)

with col1:
    team_a = st.text_input("Home Team", "Manchester United")

with col2:
