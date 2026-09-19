import json
import os
from datetime import datetime, timedelta, timezone
import streamlit as st
from styling import render_hitter_table, render_pitcher_table

st.header("팀별 선수 기록")

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)
with open("pitchers.json", "r", encoding="utf-8") as f:
    pitchers = json.load(f)

updated_at = datetime.fromtimestamp(os.path.getmtime("hitters.json"), tz=timezone(timedelta(hours=9)))
st.caption(f"🕒 최근 업데이트: {updated_at.strftime('%Y-%m-%d %H:%M')} (KST)")

team_names = []
for i in hitters:
    if i["team"] not in team_names:
        team_names.append(i["team"])

selected_team = st.radio("팀을 선택하세요", team_names, horizontal=True, key="selected_team")

team_hitters = [p for p in hitters if p["team"] == selected_team]
team_hitters.sort(key=lambda p: -p["avg"])
st.markdown(render_hitter_table(selected_team, team_hitters), unsafe_allow_html=True)

team_pitchers = [p for p in pitchers if p["team"] == selected_team]
team_pitchers.sort(key=lambda p: p["era"])
st.markdown(render_pitcher_table(selected_team, team_pitchers), unsafe_allow_html=True)
