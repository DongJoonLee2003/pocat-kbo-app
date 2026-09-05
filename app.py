import streamlit as st
import json
import subprocess
with open("players.json","w") as f:
    players = [
        {"name":"박찬호","team":"LA다저스","avg":0.289},
        {"name":"이승엽","team":"삼성라이온즈","avg":0.302},
        {"name":"류현진","team":"토론토블루제이스","avg":0.275}
    ]
    json.dump(players,f)
with open("players.json","r") as f:
    i_read = json.load(f)
    st.title("선수 정보")
    for i in i_read:
        st.write(i["name"],i["team"],i["avg"])
st.title("오늘의 KBO 경기")

if st.button("🔄 새로고침 (최신 경기 정보 가져오기)"):
    subprocess.run(["node", "fetch_games.mjs"], check=True)
    st.rerun()

with open("games.json","r", encoding="utf-8") as f:
    games = json.load(f)
    for i in games:
        if i["status"] == "SCHEDULED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ 경기 예정")
        elif i["status"] == "IN_PROGRESS":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/{i['score']['home']}:{i['score']['away']}/ 경기 진행 중")
        elif i["status"] == "FINISHED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ {i['status']} 경기종료 {i['score']['home']}:{i['score']['away']}")
        elif i["status"] == "CANCELED":
            st.write(f"{i['stadium']} /{i['home']} vs {i['away']}/ {i['startTime']}/ 경기취소")   
            
with open("hitters.json","r", encoding="utf-8") as f:
    hitters = json.load(f)
    team_names = []
    for i in hitters:
        if i["team"] not in team_names:
            team_names.append(i["team"])
    selected_team = st.radio("팀을 선택하세요", team_names)
    for player in hitters:
        if player["team"] == selected_team:
            st.write(f"{player['name']} / {player['team']} / {player['avg']}")
