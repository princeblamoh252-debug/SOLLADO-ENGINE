import streamlit as st
import requests
from datetime import datetime

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2"
API_HOST = "v3.football.api-sports.io"
TODAY = datetime.now().strftime("%Y-%m-%d") # Auto gets today's date

st.set_page_config(page_title="SOLLADO ENGINE v8.0 GLOBAL", layout="wide")
st.title("⚡ SOLLADO ENGINE v8.0 - ALL LEAGUES LIVE")
st.subheader(f"100 Matches for {TODAY}")
st.divider()

@st.cache_data(ttl=3600)
def get_all_fixtures():
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {
        "date": TODAY, # Get ALL matches today
        "timezone": "Africa/Monrovia" # Your timezone
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code!= 200:
        st.error(f"API Error: {response.status_code}")
        return []
    
    all_matches = response.json().get('response', [])
    return all_matches[:100] # LIMIT TO 100 MATCHES

fixtures = get_all_fixtures()

if len(fixtures) == 0:
    st.warning("No matches found for today. Try tomorrow or check API credits")
else:
    st.success(f"Loaded {len(fixtures)} matches from ALL leagues")
    
    fixture_options = []
    for f in fixtures:
        league = f['league']['name']
        country = f['league']['country']
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        fixture_options.append(f"[{country}] {league}: {home} vs {away}")
    
    selected_fixture = st.selectbox("Choose ANY Match from 100", fixture_options)

    if st.button("Predict Match with REAL DATA", type="primary"):
        idx = fixture_options.index(selected_fixture)
        fixture = fixtures[idx]
        
        team_a = fixture['teams']['home']['name']
        team_b = fixture['teams']['away']['name']
        league_name = fixture['league']['name']
        
        home_goals = fixture['goals']['home']
        away_goals = fixture['goals']['away']
        
        if home_goals is None:
            home_goals = 1
            away_goals = 1
            status = "UPCOMING"
        else:
            status = "LIVE/FINISHED"
        
        total_goals = home_goals + away_goals
        btts = "YES" if home_goals > 0 and away_goals > 0 else "NO"
        over_2_5 = "YES" if total_goals > 2 else "NO"
        
        st.success(f"{status}: {team_a} vs {team_b}")
        st.caption(f"League: {league_name}")
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Correct Score", f"{home_goals} - {away_goals}")
        with col2: st.metric("BTTS", btts)
        with col3: st.metric("OVER 2.5", over_2_5)
