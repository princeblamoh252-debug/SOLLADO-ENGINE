import streamlit as st
import pandas as pd

st.set_page_config(page_title="SOLLADO ENGINE v6.0", layout="wide")

st.title("⚡ SOLLADO ENGINE v6.0")
st.subheader("Stronger, Secure, No-Crash Football Predictor")

st.divider()

# STEP 3: TEAM INPUT
st.header("Step 1: Enter Teams")
col1, col2 = st.columns(2)

with col1:
    team_a = st.text_input("Home Team", "Manchester United")

with col2:
    team_b = st.text_input("Away Team", "Arsenal")

if st.button("Predict Match", type="primary"):
    st.success(f"Prediction for: {team_a} vs {team_b}")
    st.write("Step 3 Complete! Next we add the real prediction logic.")
