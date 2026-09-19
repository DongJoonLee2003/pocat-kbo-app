import json
import streamlit as st
from fetch_games import fetch_games
from styling import render_game_card

st.header("오늘의 KBO 경기")

if st.button("🔄 새로고침 (최신 경기 정보 가져오기)"):
    fetch_games()
    st.rerun()

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)

cards_html = "".join(render_game_card(g) for g in games)
st.markdown(cards_html, unsafe_allow_html=True)
