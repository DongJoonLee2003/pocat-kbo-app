import json
import os
from datetime import datetime, timedelta, timezone
import streamlit as st
from player_detail import fetch_player_detail
from styling import team_color

st.header("선수 정보")

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

col_search, col_team = st.columns([2, 1])
with col_search:
    search = st.text_input("선수 이름 검색", placeholder="예: 레이예스").strip()
with col_team:
    team_filter_options = ["전체"] + team_names
    default_team = st.session_state.get("selected_team", "전체")
    default_index = team_filter_options.index(default_team) if default_team in team_filter_options else 0
    team_filter = st.selectbox("팀으로 좁히기", team_filter_options, index=default_index)

options = [(h["name"], h["team"], h["id"], "hitter") for h in hitters if h["id"]]
options += [(p["name"], p["team"], p["id"], "pitcher") for p in pitchers if p["id"]]
if team_filter != "전체":
    options = [o for o in options if o[1] == team_filter]
if search:
    options = [o for o in options if search in o[0]]
options.sort(key=lambda o: (o[1], o[0]))

if not options:
    st.warning(f"'{search}'와 일치하는 선수가 없어요.")
    st.stop()

labels = [f"{name} ({team})" for name, team, _id, kind in options]
choice_idx = st.selectbox(f"선수를 선택하세요 ({len(options)}명)", range(len(labels)), format_func=lambda i: labels[i])

name, team, player_id, kind = options[choice_idx]
detail = fetch_player_detail(player_id, kind)
accent = team_color(team)

col1, col2 = st.columns([1, 2])
with col1:
    if detail["photo_url"]:
        st.image(detail["photo_url"], width=180)
with col2:
    st.markdown(f"<span style='font-size:20px;font-weight:800;color:{accent};'>{detail['name']}</span> ({team})", unsafe_allow_html=True)
    st.write(f"등번호: {detail['back_no']}")
    st.write(f"생년월일: {detail['birthday']}")
    st.write(f"포지션: {detail['position']}")
    st.write(f"신장/체중: {detail['height_weight']}")
    st.write(f"경력: {detail['career']}")
