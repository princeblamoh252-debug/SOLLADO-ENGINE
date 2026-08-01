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
    
    # Smart fake logic
    home_strength = random.randint(60, 90)
    away_strength = random.randint(60, 90)
    
    # 1. Win/Draw/Loss
    if home_strength > away_strength + 5:
        result = f"Home Win - {team_a} likely to win"
        likely_winner = team_a
    elif away_strength > home_strength + 5:
        result = f"Away Win - {team_b} likely to win"
        likely_winner = team_b
    else:
        result = "Draw - Very close match"
        likely_winner = "Draw"
    
    # 2. Correct Score
    home_goals = random.randint(0, 3)
    away_goals = random.randint(0, 3)
    correct_score = f"{home_goals} - {away_goals}"
    
    # 3. Expected Goals
    xG_home = round(random.uniform(0.8, 2.5), 2)
    xG_away = round(random.uniform(0.8, 2.5), 2)
    
    # 4. Over/Under
    total_goals = home_goals + away_goals
    over_1_5 = "OVER 1.5 ✅" if total_goals > 1 else "UNDER 1.5 ❌"
    over_2_5 = "OVER 2.5 ✅" if total_goals > 2 else "UNDER 2.5 ❌"
    
    st.success(f"🎯 RESULT: {result}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct Score", correct_score)
    with col2:
        st.metric(f"xG {team_a}", xG_home)
    with col3:
        st.metric(f"xG {team_b}", xG_away)
    
    st.write(f"**Over/Under:** {over_1_5} | {over_2_5}")
    st.metric("Confidence", f"{random.randint(60, 88)}%")
    
    st.info("Step 4.5 Complete! Next we add real data with API")
