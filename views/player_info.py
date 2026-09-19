import json
import streamlit as st
from player_detail import fetch_player_detail
from styling import team_color

st.header("선수 정보")

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)
with open("pitchers.json", "r", encoding="utf-8") as f:
    pitchers = json.load(f)

options = [(h["name"], h["team"], h["id"], "hitter") for h in hitters if h["id"]]
options += [(p["name"], p["team"], p["id"], "pitcher") for p in pitchers if p["id"]]
options.sort(key=lambda o: (o[1], o[0]))

labels = [f"{name} ({team})" for name, team, _id, kind in options]
choice_idx = st.selectbox("선수를 선택하세요", range(len(labels)), format_func=lambda i: labels[i])

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
