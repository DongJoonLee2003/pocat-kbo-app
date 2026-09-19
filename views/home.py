import json
from datetime import datetime, timedelta, timezone
import streamlit as st
from styling import render_stadium_hero

try:
    with open("games.json", "r", encoding="utf-8") as f:
        games = json.load(f)
except FileNotFoundError:
    games = []

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)

live_games = sum(1 for g in games if g["status"] == "IN_PROGRESS")
kst_now = datetime.now(timezone(timedelta(hours=9)))
today_label = kst_now.strftime("%Y.%m.%d (%a)")

st.markdown(render_stadium_hero(today_label, len(games), live_games), unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3)
col1.metric("오늘 경기 수", f"{len(games)}경기")
col2.metric("등록 타자 수", f"{len(hitters)}명")
col3.metric("등록 구단 수", "10개")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.page_link("views/today_games.py", label="⚾ 오늘 KBO 경기", use_container_width=True)
with c2:
    st.page_link("views/team_stats.py", label="📊 팀별 선수 기록", use_container_width=True)
with c3:
    st.page_link("views/player_info.py", label="🧑 선수 정보", use_container_width=True)
