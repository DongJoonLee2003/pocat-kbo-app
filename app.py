import streamlit as st
import json
from fetch_games import fetch_games
from player_detail import fetch_player_detail
from styling import PAGE_CSS, team_color, render_game_card, render_hitter_table, render_pitcher_table

st.set_page_config(page_title="PoCaT KBO", layout="wide")
st.markdown(PAGE_CSS, unsafe_allow_html=True)

st.title("PoCaT KBO")

# ── 오늘의 KBO 경기 (카드형) ──────────────────────────────
st.header("오늘의 KBO 경기")

if st.button("🔄 새로고침 (최신 경기 정보 가져오기)"):
    fetch_games()
    st.rerun()

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)

cards_html = "".join(render_game_card(g) for g in games)
st.markdown(cards_html, unsafe_allow_html=True)

# ── 팀별 선수 기록 (표 + 팀컬러) ──────────────────────────────
st.header("팀별 선수 기록")

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)
with open("pitchers.json", "r", encoding="utf-8") as f:
    pitchers = json.load(f)

team_names = []
for i in hitters:
    if i["team"] not in team_names:
        team_names.append(i["team"])

selected_team = st.radio("팀을 선택하세요", team_names, horizontal=True)

team_hitters = [p for p in hitters if p["team"] == selected_team]
team_hitters.sort(key=lambda p: -p["avg"])
st.markdown(render_hitter_table(selected_team, team_hitters), unsafe_allow_html=True)

team_pitchers = [p for p in pitchers if p["team"] == selected_team]
team_pitchers.sort(key=lambda p: p["era"])
st.markdown(render_pitcher_table(selected_team, team_pitchers), unsafe_allow_html=True)

# ── 선수 상세보기 (사진/프로필) ──────────────────────────────
st.header("선수 상세보기")

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
