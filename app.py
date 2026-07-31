import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

st.set_page_config(page_title="SOLLADO ENGINE v5.0", layout="wide")
st.title("⚽ SOLLADO ENGINE v5.0")
st.caption("Effectiveness + Consistency Predictor. Just type team names.")

HEADERS = {'User-Agent': 'Mozilla/5.0'}

@st.cache_data
def find_team_url(team_name):
    search_url = f"https://fbref.com/search/search.fcgi?search={team_name.replace(' ', '+')}"
    r = requests.get(search_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'lxml')
    link = soup.find('div', class_='search-item-name').find('a')['href']
    return "https://fbref.com" + link

@st.cache_data
def get_last5_stats(team_url):
    r = requests.get(team_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'id': 'matchlogs_for'})
    df = pd.read_html(str(table))[0].head(5)

    gf = df['GF'].astype(float).sum()
    ga = df['GA'].astype(float).sum()
    xg = df['xG'].astype(float).sum()
    xga = df['xGA'].astype(float).sum()
    sot = df['SoT'].astype(float).sum()
    shots = df['Sh'].astype(float).sum()
    wins = (df['Result'] == 'W').sum()
    draws = (df['Result'] == 'D').sum()
    cs = (df['GA'] == 0).sum()
    stdev = df['GF'].astype(float).std()

    return {
        "xG5": xg, "GF5": gf, "GA5": ga, "xGA5": xga,
        "SoT%": sot/shots if shots>0 else 0.4, "CS5": cs,
        "Form5": wins*3 + draws, "STDEV": stdev if stdev>0 else 0.5
    }

def predict(home_name, away_name):
    with st.spinner(f'Fetching {home_name} data...'):
        H = get_last5_stats(find_team_url(home_name))
    with st.spinner(f'Fetching {away_name} data...'):
        A = get_last5_stats(find_team_url(away))
