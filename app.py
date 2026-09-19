import streamlit as st
import json
from fetch_games import fetch_games
from player_detail import fetch_player_detail

st.title("PoCaT KBO")

# ── 오늘의 KBO 경기 ──────────────────────────────
st.header("오늘의 KBO 경기")

if st.button("🔄 새로고침 (최신 경기 정보 가져오기)"):
    fetch_games()
    st.rerun()

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)
    for i in games:
        if i["status"] == "SCHEDULED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ 경기 예정")
        elif i["status"] == "IN_PROGRESS":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/{i['score']['home']}:{i['score']['away']}/ 경기 진행 중")
        elif i["status"] == "FINISHED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ 경기종료 {i['score']['home']}:{i['score']['away']}")
        elif i["status"] == "CANCELED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ 경기취소")

# ── 팀별 선수 기록 ──────────────────────────────
st.header("팀별 선수 기록")

with open("hitters.json", "r", encoding="utf-8") as f:
    hitters = json.load(f)
with open("pitchers.json", "r", encoding="utf-8") as f:
    pitchers = json.load(f)

team_names = []
for i in hitters:
    if i["team"] not in team_names:
        team_names.append(i["team"])

selected_team = st.radio("팀을 선택하세요", team_names)

st.subheader(f"{selected_team} 타자")
for player in hitters:
    if player["team"] == selected_team:
        st.write(
            f"{player['name']} · 타율 {player['avg']} · {player['g']}경기 · "
            f"안타 {player['h']}(2루타 {player['double']}, 3루타 {player['triple']}, 홈런 {player['hr']}) · 타점 {player['rbi']}"
        )

st.subheader(f"{selected_team} 투수")
for pitcher in pitchers:
    if pitcher["team"] == selected_team:
        st.write(
            f"{pitcher['name']} · 평균자책점 {pitcher['era']} · {pitcher['w']}승 {pitcher['l']}패 "
            f"{pitcher['sv']}세이브 {pitcher['hld']}홀드 · 탈삼진 {pitcher['so']} · WHIP {pitcher['whip']}"
        )

# ── 선수 상세보기 (사진/프로필) ──────────────────────────────
st.header("선수 상세보기")

options = [(h["name"], h["team"], h["id"], "hitter") for h in hitters if h["id"]]
options += [(p["name"], p["team"], p["id"], "pitcher") for p in pitchers if p["id"]]
options.sort(key=lambda o: (o[1], o[0]))

labels = [f"{name} ({team})" for name, team, _id, kind in options]
choice_idx = st.selectbox("선수를 선택하세요", range(len(labels)), format_func=lambda i: labels[i])

name, team, player_id, kind = options[choice_idx]
detail = fetch_player_detail(player_id, kind)

col1, col2 = st.columns([1, 2])
with col1:
    if detail["photo_url"]:
        st.image(detail["photo_url"], width=180)
with col2:
    st.write(f"**{detail['name']}** ({team})")
    st.write(f"등번호: {detail['back_no']}")
    st.write(f"생년월일: {detail['birthday']}")
    st.write(f"포지션: {detail['position']}")
    st.write(f"신장/체중: {detail['height_weight']}")
    st.write(f"경력: {detail['career']}")
