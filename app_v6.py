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
    team_b = st.text_input("Away Team", "Arsenal")

if st.button("Predict Match", type="primary"):
    
    # LOCK THE RANDOMNESS - Same teams = Same result
    seed = hash(team_a + team_b) 
    random.seed(seed)
    
    home_strength = random.randint(60, 90)
    away_strength = random.randint(60, 90)
    
    # 1. WINNER OF THE MATCH
    if home_strength > away_strength + 5:
        winner = f"{team_a} WIN"
        winner_tip = f"✅ Back {team_a}"
    elif away_strength > home_strength + 5:
        winner = f"{team_b} WIN"
        winner_tip = f"✅ Back {team_b}"
    else:
        winner = "DRAW"
        winner_tip = "⚠️ Avoid Winner Market - Too Close"
    
    # 2. DOUBLE CHANCE MARKETS
    if home_strength >= away_strength:
        double_chance_1X = f"1X - {team_a
