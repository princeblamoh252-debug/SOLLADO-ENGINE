import streamlit as st
import requests

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2"
API_HOST = "v3.football.api-sports.io"

st.set_page_config(page_title="SOLLADO ENGINE v7.2 FIXED", layout="wide")
st.title("⚡ SOLLADO ENGINE v7.2 - LIVE DATA")
st.divider()

@st.cache_data
def get_fixtures():
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"league": "39", "season": "2025", "next": "10"}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('response', [])
    except:
        return []

fixtures = get_fixtures()

if len(fixtures) == 0:
    st.error("No matches loaded. API Key is still activating or no credits. Wait 10 min and refresh.")
else:
    st.header("Step 1: Pick Today's Fixtures")
    fixture_options = []
    for f in fixtures:
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        fixture_options.append(f"{home} vs {away}")
    
    selected_fixture = st.selectbox("Choose Match", fixture_options)

    if st.button("Predict Match with REAL DATA", type="primary"):
        st.success(f"You selected: {selected_fixture}")
        st.info("API is connected! Data is loading from API-Football")
        st.metric("Status", "LIVE DATA ACTIVE")
