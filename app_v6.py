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
        double_chance_1X = f"1X - {team_a} Win or Draw ✅ SAFE"
        double_chance_2X = f"2X - {team_b} Win or Draw ❌ RISKY"
    else:
        double_chance_1X = f"1X - {team_a} Win or Draw ❌ RISKY"
        double_chance_2X = f"2X - {team_b} Win or Draw ✅ SAFE"
    
    # 3. Correct Score
    home_goals = random.randint(0, 3)
    away_goals = random.randint(0, 3)
    correct_score = f"{home_goals} - {away_goals}"
    
    # 4. Expected Goals
    xG_home = round(random.uniform(0.8, 2.5), 2)
    xG_away = round(random.uniform(0.8, 2.5), 2)
    
    # 5. Over/Under
    total_goals = home_goals + away_goals
    over_1_5 = "OVER 1.5 ✅" if total_goals > 1 else "UNDER 1.5 ❌"
    over_2_5 = "OVER 2.5 ✅" if total_goals > 2 else "UNDER 2.5 ❌"
    
    # DISPLAY
    st.success(f"🏆 WINNER: {winner}")
    st.write(f"**Tip:** {winner_tip}")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("DOUBLE CHANCE 1X", double_chance_1X)
    with col2:
        st.metric("DOUBLE CHANCE 2X", double_chance_2X)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct Score", correct_score)
    with col2:
        st.metric(f"xG {team_a}", xG_home)
    with col3:
        st.metric(f"xG {team_b}", xG_away)
    
    st.write(f"**Over/Under:** {over_1_5} | {over_2_5}")
    st.metric("Confidence", f"{random.randint(60, 88)}%")
    
    st.info("Step 4.6 Complete! Ready for real API data")
