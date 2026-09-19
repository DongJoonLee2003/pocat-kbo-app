import json
import streamlit as st

st.title("PoCaT KBO")
st.write("오늘 경기 결과와 선수 기록을 한눈에 확인하세요.")

try:
    with open("games.json", "r", encoding="utf-8") as f:
        games = json.load(f)
except FileNotFoundError:
    games = []

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)

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
