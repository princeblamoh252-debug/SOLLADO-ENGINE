import streamlit as st
import requests
import hashlib
from datetime import datetime, timedelta

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2"
API_HOST = "v3.football.api-sports.io"

st.set_page_config(page_title="SOLLADO ENGINE v9.3", layout="wide")
st.title("⚡ SOLLADO ENGINE v9.3 - 7 DAY SCANNER")

# ===== DATE PICKER + SEED =====
col1, col2 = st.columns([2,1])
with col1:
    selected_date = st.date_input("📅 Pick Start Date", value=datetime.now() + timedelta(days=1))
with col2:
    SEED = st.text_input("🔒 ENGINE SEED", value="SOLLADO2026")

START_DATE = selected_date.strftime("%Y-%m-%d")
END_DATE = (selected_date + timedelta(days=6)).strftime("%Y-%m-%d") # 7 days total

st.subheader(f"Predictions from {START_DATE} to {END_DATE} - All Leagues")
st.divider()

@st.cache_data(ttl=86400) # Cache for 24hrs
def get_fixtures_7days(start_date):
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")
    
    params = {
        "from": start_date,
        "to": end_date, 
        "timezone": "Africa/Monrovia"
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code!= 200:
        st.error(f"API Error: {response.status_code}")
        return []
        
    all_matches = response.json().get('response', [])
    return all_matches[:100] # Limit to 100 to save requests

def locked_predict(team_a_id, team_b_id, seed, match_date):
    # 100% Consistent: Same teams + date + seed = Same result forever
    unique_string = f"{team_a_id}-{team_b_id}-{seed}-{match_date}"
    hash_object = hashlib.md5(unique_string.encode())
    hash_number = int(hash_object.hexdigest(), 16)
    home_goals = (hash_number % 4)
    away_goals = ((hash_number // 10) % 4)
    return home_goals, away_goals

fixtures = get_fixtures_7days(START_DATE)

if len(fixtures) == 0:
    st.warning(f"😴 No matches found from {START_DATE} to {END_DATE}. Free API can be 2-3 days late for new season.")
else:
    st.success(f"✅ Loaded {len(fixtures)} matches from next 7 days")
    
    fixture_options = []
    for f in fixtures:
        date = f['fixture']['date'][:10]
        time = f['fixture']['date'][11:16]
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        country = f['league']['country']
        fixture_options.append(f"[{date} {time}] [{country}] {home} vs {away} | {league}")
    
    selected_fixture = st.selectbox("Pick a Match to Predict", fixture_options)

    if st.button("GENERATE LOCKED PREDICTION", type="primary"):
        idx = fixture_options.index(selected_fixture)
        fixture = fixtures[idx]
        
        team_a = fixture['teams']['home']['name']
        team_b = fixture['teams']['away']['name']
        team_a_id = fixture['teams']['home']['id']
        team_b_id = fixture['teams']['away']['id']
        match_date = fixture['fixture']['date'][:10]
        
        pred_home, pred_away = locked_predict(team_a_id, team_b_id, SEED, match_date)
        total = pred_home + pred_away
        
        btts = "YES" if pred_home > 0 and pred_away > 0 else "NO"
        over_2_5 = "YES" if total > 2.5 else "NO"
        
        st.success(f"LOCKED PREDICTION: {team_a} vs {team_b}")
        st.caption(f"Date: {match_date} | Seed: {SEED}")
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Exact Score", f"{pred_home} - {pred_away}")
        with col2: st.metric("BTTS", btts)
        with col3: st.metric("OVER 2.5", over_2_5)
