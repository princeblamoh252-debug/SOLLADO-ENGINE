import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2"
API_HOST = "v3.football.api-sports.io"

st.set_page_config(page_title="SOLLADO ENGINE v9.2", layout="wide")
st.title("⚡ SOLLADO ENGINE v9.2 - DATE SELECTOR")

# ===== DATE PICKER =====
col1, col2 = st.columns([2,1])
with col1:
    selected_date = st.date_input("📅 Pick Any Match Date", value=datetime.now())
with col2:
    SEED = st.text_input("🔒 ENGINE SEED", value="SOLLADO2026")

DATE_TO_USE = selected_date.strftime("%Y-%m-%d")
st.subheader(f"Predictions for {DATE_TO_USE} - All Leagues")
st.divider()

@st.cache_data(ttl=86400) # Cache for 24hrs per date
def get_fixtures_for_date(date):
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"date": date, "timezone": "Africa/Monrovia"} # Gets ALL matches that day
    response = requests.get(url, headers=headers, params=params)
    all_matches = response.json().get('response', [])
    return all_matches[:100] # Limit to 100

def locked_predict(team_a_id, team_b_id, seed, date):
    # This makes the prediction 100% consistent for same teams + date + seed
    unique_string = f"{team_a_id}-{team_b_id}-{seed}-{date}"
    hash_object = hashlib.md5(unique_string.encode())
    hash_number = int(hash_object.hexdigest(), 16)
    home_goals = (hash_number % 4)
    away_goals = ((hash_number // 10) % 4)
    return home_goals, away_goals

fixtures = get_fixtures_for_date(DATE_TO_USE)

if len(fixtures) == 0:
    st.warning(f"😴 No matches found for {DATE_TO_USE}. Try another date like weekend.")
else:
    st.success(f"✅ Loaded {len(fixtures)} matches for {DATE_TO_USE}")
    
    fixture_options = []
    for f in fixtures:
        time = f['fixture']['date'][11:16]
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        fixture_options.append(f"[{time}] {home} vs {away} | {league}")
    
    selected_fixture = st.selectbox("Pick a Match to Predict", fixture_options)

    if st.button("GENERATE LOCKED PREDICTION", type="primary"):
        idx = fixture_options.index(selected_fixture)
        fixture = fixtures[idx]
        
        team_a = fixture['teams']['home']['name']
        team_b = fixture['teams']['away']['name']
        team_a_id = fixture['teams']['home']['id']
        team_b_id = fixture['teams']['away']['id']
        
        pred_home, pred_away = locked_predict(team_a_id, team_b_id, SEED, DATE_TO_USE)
        total = pred_home + pred_away
        
        btts = "YES" if pred_home > 0 and pred_away > 0 else "NO"
        over_2_5 = "YES" if total > 2.5 else "NO"
        
        st.success(f"LOCKED PREDICTION: {team_a} vs {team_b}")
        st.caption(f"Date: {DATE_TO_USE} | Seed: {SEED}")
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Exact Score", f"{pred_home} - {pred_away}")
        with col2: st.metric("BTTS", btts)
        with col3: st.metric("OVER 2.5", over_2_5)
