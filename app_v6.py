import streamlit as st
import pandas as pd
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
    team_b = st.text_input("Away Team", "Arsenal")

if st.button("Predict Match", type="primary"):
    # Step 4: Smart Prediction Logic
    outcomes = ["Home Win", "Draw", "Away Win"]
    prediction = random.choice(outcomes)
    confidence = random.randint(55, 85)
    
    st.success(f"🎯 PREDICTION: {prediction}")
    st.metric("Confidence", f"{confidence}%")
    st.write(f"**Match:** {team_a} vs {team_b}")
    st.info("Step 4 Complete! Next we connect real football data.")
