import json
from datetime import datetime, timedelta, timezone
import streamlit as st
from fetch_games import fetch_games
from styling import render_game_card

st.header("오늘의 KBO 경기")

if st.button("🔄 새로고침 (최신 경기 정보 가져오기)"):
    fetch_games()
    st.rerun()

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)
with open("pitchers.json", "r", encoding="utf-8") as f:
    pitchers = json.load(f)

if games:
    game_date = datetime.strptime(games[0]["date"], "%Y%m%d")
else:
    game_date = datetime.now(timezone(timedelta(hours=9)))

weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][game_date.weekday()]
st.caption(f"📅 {game_date.strftime('%Y년 %m월 %d일')} ({weekday_kr}) 경기 · 새로고침 시각 기준")

cards_html = "".join(render_game_card(g, pitchers) for g in games)
st.markdown(cards_html, unsafe_allow_html=True)
