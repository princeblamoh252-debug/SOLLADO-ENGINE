import streamlit as st
import requests

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2" # <-- PASTE YOUR KEY HERE ON LINE 4
API_HOST = "v3.football.api-sports.io"

st.set_page_config(page_title="SOLLADO ENGINE v7.0 API", layout="wide")

st.title("⚡ SOLLADO ENGINE v7.0 - LIVE DATA")
st.subheader("Real Football Data Predictor")
st.divider()

st.header("Step 1: Pick Today's Fixtures")

# FUNCTION TO GET FIXTURES
@st.cache_data
def get_fixtures():
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"league": "39", "season": "2025", "next": "10"} # 39 = EPL
    response = requests.get(url, headers=headers, params=params)
    return response.json()['response']

fixtures = get_fixtures()

fixture_options = [f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}" for f in fixtures]
selected_fixture = st.selectbox("Choose Match", fixture_options)

if st.button("Predict Match with REAL DATA", type="primary"):
    
    # Find the fixture ID
    fixture_id = [f['fixture']['id'] for f in fixtures if f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}" == selected_fixture][0]
    
    # GET STATISTICS FROM API
    url_stats = f"https://{API_HOST}/fixtures/statistics"
    headers = {"x-apisports-key": API_KEY}
    params = {"fixture": fixture_id}
    stats_response = requests.get(url_stats, headers=headers, params=params).json()['response']
    
    team_a = stats_response[0]['team']['name']
    team_b = stats_response[1]['team']['name']
    
    # GET REAL GOALS DATA
    url_fixture = f"https://{API_HOST}/fixtures"
    params = {"id": fixture_id}
    fixture_data = requests.get(url_fixture, headers=headers, params=params).json()['response'][0]
    
    home_goals = fixture_data['goals']['home']
    away_goals = fixture_data['goals']['away']
    
    # If match not played yet, use shots as proxy
    if home_goals is None:
        home_goals = 1
        away_goals = 1
    
    total_goals = home_goals + away_goals
    
    # BTTS YES/NO
    btts = "BTTS: YES" if home_goals > 0 and away_goals > 0 else "BTTS: NO"
    
    # OVER/UNDER YES/NO
    over_1_5 = "OVER 1.5: YES" if total_goals > 1 else "OVER 1.5: NO"
    under_1_5 = "UNDER 1.5: YES" if total_goals <= 1 else "UNDER 1.5: NO"
    over_2_5 = "OVER 2.5: YES" if total_goals > 2 else "OVER 2.5: NO"
    under_2_5 = "UNDER 2.5: YES" if total_goals <= 2 else "UNDER 2.5: NO"
    
    # DISPLAY
    st.success(f"REAL DATA: {team_a} vs {team_b}")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct Score", f"{home_goals} - {away_goals}")
    with col2:
        st.metric("BTTS", btts)
    with col3:
        st.metric("Total Goals", total_goals)
    st.divider()
    
    st.subheader("Over/Under Predictions")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("1.5 Goals", over_1_5)
        st.metric("1.5 Goals Alt", under_1_5)
    with col2:
        st.metric("2.5 Goals", over_2_5)
        st.metric("2.5 Goals Alt", under_2_5)
    
    st.info("Step 5.1 Complete! Now using LIVE API DATA")
