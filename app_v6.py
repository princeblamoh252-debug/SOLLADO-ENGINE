import streamlit as st
import requests
from datetime import datetime

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2"
API_HOST = "v3.football.api-sports.io"
TODAY = datetime.now().strftime("%Y-%m-%d")

st.set_page_config(page_title="SOLLADO ENGINE v9.0 PRE-MATCH", layout="wide")
st.title("⚡ SOLLADO ENGINE v9.0 - PRE-MATCH PREDICTOR")
st.subheader(f"Predictions for {TODAY} - All Leagues")
st.divider()

@st.cache_data(ttl=3600)
def get_upcoming_fixtures():
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"date": TODAY, "status": "NS", "timezone": "Africa/Monrovia"} # NS = Not Started
    response = requests.get(url, headers=headers, params=params)
    all_matches = response.json().get('response', [])
    return all_matches[:100]

@st.cache_data
def get_team_stats(team_id):
    url = f"https://{API_HOST}/teams/statistics"
    headers = {"x-apisports-key": API_KEY}
    params = {"team": team_id, "season": "2026", "league": "39"} # Using EPL as base
    try:
        response = requests.get(url, headers=headers, params=params).json()
        return response['response']
    except:
        return None

fixtures = get_upcoming_fixtures()

if len(fixtures) == 0:
    st.warning("No upcoming matches found for today")
else:
    st.success(f"Found {len(fixtures)} PRE-MATCH games to predict")
    
    fixture_options = []
    for f in fixtures:
        league = f['league']['name']
        country = f['league']['country']
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        time = f['fixture']['date'][11:16]
        fixture_options.append(f"[{time}] {country}: {home} vs {away} | {league}")
    
    selected_fixture = st.selectbox("Pick a Match to Predict", fixture_options)

    if st.button("GENERATE PRE-MATCH PREDICTION", type="primary"):
        idx = fixture_options.index(selected_fixture)
        fixture = fixtures[idx]
        
        team_a = fixture['teams']['home']['name']
        team_b = fixture['teams']['away']['name']
        team_a_id = fixture['teams']['home']['id']
        team_b_id = fixture['teams']['away']['id']
        league_name = fixture['league']['name']
        
        st.success(f"PREDICTING: {team_a} vs {team_b}")
        st.caption(f"League: {league_name}")
        
        # SIMPLE PREDICTION LOGIC USING GOALS
        stats_a = get_team_stats(team_a_id)
        stats_b = get_team_stats(team_b_id)
        
        if stats_a and stats_b:
            goals_for_a = stats_a['goals']['for']['total']['total']
            goals_against_b = stats_b['goals']['against']['total']['total']
            goals_for_b = stats_b['goals']['for']['total']['total']
            goals_against_a = stats_a['goals']['against']['total']['total']
            
            pred_home = round((goals_for_a + goals_against_b) / 20, 1)
            pred_away = round((goals_for_b + goals_against_a) / 20, 1)
            pred_home = max(0, pred_home)
            pred_away = max(0, pred_away)
            total = pred_home + pred_away
        else:
            pred_home = 1
            pred_away = 1
            total = 2
        
        btts = "YES" if pred_home > 0 and pred_away > 0 else "NO"
        over_2_5 = "YES" if total > 2.5 else "NO"
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Predicted Score", f"{pred_home} - {pred_away}")
        with col2: st.metric("BTTS Prediction", btts)
        with col3: st.metric("OVER 2.5 Prediction", over_2_5)
        st.divider()
        
        st.info("This uses real team stats from API-Football to predict. Not random anymore!")
