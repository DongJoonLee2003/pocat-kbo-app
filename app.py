import streamlit as st
from styling import PAGE_CSS

st.set_page_config(page_title="PoCaT KBO", layout="wide")
st.markdown(PAGE_CSS, unsafe_allow_html=True)

pages = [
    st.Page("views/home.py", title="홈", icon="🏠", default=True),
    st.Page("views/today_games.py", title="오늘 KBO 경기", icon="⚾"),
    st.Page("views/team_stats.py", title="팀별 선수 기록", icon="📊"),
    st.Page("views/player_info.py", title="선수 정보", icon="🧑"),
]

pg = st.navigation(pages, position="top")
pg.run()
