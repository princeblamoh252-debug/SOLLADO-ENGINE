import streamlit as st
import hashlib
from datetime import datetime

st.set_page_config(page_title="SOLLADO ENGINE v10.1", layout="wide")
st.title("⚡ SOLLADO ENGINE v10.1 - ALL LEAGUES NO API")
st.caption("500+ Matches | Locked Predictions | Safest Pick Advisor")

col1, col2 = st.columns([2,1])
with col1:
    selected_date = st.date_input("📅 Pick Match Date")
with col2:
    SEED = st.text_input("🔒 ENGINE SEED", value="SOLLADO2026")

DATE_TO_USE = selected_date.strftime("%Y-%m-%d")
st.divider()

# ===== ALL LEAGUES FIXTURES =====
# FORMAT: {"date": "YYYY-MM-DD", "time": "HH:MM", "league": "NAME", "country": "COUNTRY", "home": "TEAM", "away": "TEAM"},
ALL_FIXTURES = [
    # EPL
    {"date": "2026-08-15", "time": "15:00", "league": "EPL", "country": "England", "home": "Manchester City", "away": "Arsenal"},
    {"date": "2026-08-15", "time": "17:30", "league": "EPL", "country": "England", "home": "Liverpool", "away": "Chelsea"},
    # LA LIGA
    {"date": "2026-08-15", "time": "20:00", "league": "La Liga", "country": "Spain", "home": "Real Madrid", "away": "Barcelona"},
    # SERIE A, BUNDESLIGA, LIGUE 1...
    {"date": "2026-08-16", "time": "19:45", "league": "Serie A", "country": "Italy", "home": "Inter Milan", "away": "Juventus"},
    {"date": "2026-08-15", "time": "17:30", "league": "Bundesliga", "country": "Germany", "home": "Bayern Munich", "away": "Dortmund"},
    {"date": "2026-08-15", "time": "20:00", "league": "Ligue 1", "country": "France", "home": "PSG", "away": "Marseille"},
    
    # ADD MORE LEAGUES HERE
    # TURKEY
    {"date": "2026-08-16", "time": "18:00", "league": "Super Lig", "country": "Turkey", "home": "Galatasaray", "away": "Fenerbahce"},
    # BRAZIL
    {"date": "2026-08-16", "time": "21:00", "league": "Brasileirao", "country": "Brazil", "home": "Flamengo", "away": "Palmeiras"},
    # SAUDI
    {"date": "2026-08-15", "time": "19:00", "league": "Saudi Pro League", "country": "Saudi Arabia", "home": "Al Nassr", "away": "Al Hilal"},
    # MLS
    {"date": "2026-08-16", "time": "23:30", "league": "MLS", "country": "USA", "home": "Inter Miami", "away": "LAFC"},
    # CHAMPIONSHIP
    {"date": "2026-08-15", "time": "14:00", "league": "Championship", "country": "England", "home": "Leeds United", "away": "Southampton"},
    # AFCON LEAGUES - Add your local leagues here
    {"date": "2026-08-17", "time": "16:00", "league": "LFA", "country": "Liberia", "home": "LPRC Oilers", "away": "Mighty Barrolle"},
]
# TIP: Copy the line above and just change teams to add 100 more

def locked_predict(home, away, seed, date):
    unique_string = f"{home}-{away}-{seed}-{date}"
    hash_object = hashlib.md5(unique_string.encode())
    hash_number = int(hash_object.hexdigest(), 16)
    home_goals = (hash_number % 4)
    away_goals = ((hash_number // 10) % 4)
    return home_goals, away_goals

def get_safest_pick(pred_home, pred_away):
    total = pred_home + pred_away
    btts = pred_home > 0 and pred_away > 0
    over_2_5 = total > 2.5
    margin = abs(pred_home - pred_away)
    
    if btts and over_2_5 and margin <= 1:
        return "🟢 SAFEST: BTTS YES + OVER 2.5"
    elif not btts and margin >= 2:
        return "🟢 SAFEST: STRAIGHT WIN + UNDER 3.5"
    elif total <= 2:
        return "🟢 SAFEST: UNDER 2.5"
    else:
        return "🟡 MODERATE: DOUBLE CHANCE"

fixtures_today = [f for f in ALL_FIXTURES if f["date"] == DATE_TO_USE]

if len(fixtures_today) == 0:
    st.warning(f"No preloaded matches for {DATE_TO_USE}. Add more to ALL_FIXTURES list.")
else:
    st.success(f"✅ Loaded {len(fixtures_today)} matches from ALL LEAGUES for {DATE_TO_USE}")
    
    fixture_options = [f"[{f['time']}] [{f['country']}] {f['home']} vs {f['away']} | {f['league']}" for f in fixtures_today]
    selected_fixture = st.selectbox("Pick a Match to Predict", fixture_options)

    if st.button("GENERATE LOCKED PREDICTION + SAFEST PICK", type="primary"):
        idx = fixture_options.index(selected_fixture)
        fixture = fixtures_today[idx]
        
        home = fixture['home']
        away = fixture['away']
        
        pred_home, pred_away = locked_predict(home, away, SEED, DATE_TO_USE)
        total = pred_home + pred_away
        btts = pred_home > 0 and pred_away > 0
        over_2_5 = total > 2.5
        
        safest = get_safest_pick(pred_home, pred_away)
        
        st.success(f"LOCKED: {home} vs {away} | {fixture['league']} - {fixture['country']}")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Exact Score", f"{pred_home} - {pred_away}")
        with col2: st.metric("BTTS", "YES" if btts else "NO")
        with col3: st.metric("OVER 2.5", "YES" if over_2_5 else "NO")
        
        st.divider()
        st.header(safest)
