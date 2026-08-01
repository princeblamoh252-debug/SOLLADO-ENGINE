import streamlit as st
import requests

API_KEY = "5d69ec78a711ae5e9d031a0e13286ce2" # YOUR KEY IS HERE
API_HOST = "v3.football.api-sports.io"

st.set_page_config(page_title="SOLLADO ENGINE v7.1 API", layout="wide")
st.title("⚡ SOLLADO ENGINE v7.1 - LIVE DATA")
st.subheader("Real Football Data Predictor")
st.divider()

@st.cache_data
def get_fixtures():
    url = f"https://{API_HOST}/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"league": "39", "season": "2025", "next": "10"} # EPL
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code!= 200:
        st.error(f"API Error: {response.status_code}. Check your API Key credits")
        return []
    return response.json().get('response', [])

fixtures = get_fixtures()

if not fixtures:
    st.warning("No fixtures found. API Key might still be activating. Wait 5 min and refresh")
else:
    st.header("Step 1: Pick Today's Fixtures")
    fixture_options = [f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}" for f in fixtures]
    selected_fixture = st.selectbox("Choose Match", fixture_options)

    if st.button("Predict Match with REAL DATA", type="primary"):
        fixture_id = [f['fixture']['id'] for f in fixtures if f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}" == selected_fixture][0]
        
        # GET REAL DATA
        url_fixture = f"https
