import html

TEAM_COLORS = {
    "KT": "#EB1C24",
    "삼성": "#074CA1",
    "LG": "#C30452",
    "KIA": "#EA0029",
    "두산": "#131230",
    "NC": "#1D4F91",
    "롯데": "#041E42",
    "SSG": "#CE0E2D",
    "한화": "#FF6600",
    "키움": "#820024",
}
DEFAULT_ACCENT = "#1d6f52"

PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=Oswald:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

.kbo-game-card{
    background:#0d1b14; border:1px solid #1f3c2c; border-radius:12px;
    padding:14px 18px; margin-bottom:10px; color:#eef4ee;
    font-family:'Noto Sans KR',sans-serif;
    display:flex; justify-content:space-between; align-items:center; gap:14px;
}
.kbo-game-card .vs{font-family:'Oswald',sans-serif; font-weight:700; font-size:17px; letter-spacing:.01em;}
.kbo-game-card .stadium{font-size:11px; color:#8fae9c; margin-top:2px;}
.kbo-game-card .right{text-align:right;}
.kbo-game-card .time{font-size:12px; color:#8fae9c;}
.kbo-game-card .score{font-family:'Oswald',sans-serif; font-size:22px; color:#5fe0a0; font-variant-numeric:tabular-nums;}
.kbo-game-card .status{font-size:11px; font-weight:600; letter-spacing:.02em;}
.kbo-game-card .status.live{color:#5fe0a0;}
.kbo-game-card .status.done{color:#8fae9c;}
.kbo-game-card .status.cancel{color:#e07b6a;}

.kbo-team-band{
    padding:11px 18px; border-radius:10px 10px 0 0;
    font-family:'Oswald',sans-serif; font-size:16px; letter-spacing:.02em; color:#fff;
    display:flex; justify-content:space-between; align-items:baseline;
}
.kbo-team-band .n{font-size:11px; font-family:'Noto Sans KR',sans-serif; font-weight:600; opacity:.85;}
.kbo-table-wrap{border:1px solid #e4e7eb; border-top:none; border-radius:0 0 10px 10px; overflow:hidden; margin-bottom:26px;}
table.kbo-table{width:100%; border-collapse:collapse; font-size:12.5px; background:#fff;}
table.kbo-table th{
    text-align:right; font-weight:600; color:#6b7480; font-size:11px;
    padding:8px 10px; border-bottom:1px solid #e4e7eb; white-space:nowrap;
}
table.kbo-table th:first-child, table.kbo-table td:first-child{text-align:left;}
table.kbo-table td{
    text-align:right; padding:7px 10px; border-bottom:1px solid #eef0f2;
    font-family:'IBM Plex Mono',monospace; font-variant-numeric:tabular-nums; color:#2a2d31;
}
table.kbo-table td:first-child{font-family:'Noto Sans KR',sans-serif; font-weight:600; color:#15181c;}
table.kbo-table tr:last-child td{border-bottom:none;}
</style>
"""


def team_color(team):
    return TEAM_COLORS.get(team, DEFAULT_ACCENT)


def render_game_card(g):
    e = html.escape
    if g["status"] == "SCHEDULED":
        right = f'<div class="status">경기 예정</div><div class="time">{e(g["startTime"])}</div>'
    elif g["status"] == "IN_PROGRESS":
        right = f'<div class="score">{g["score"]["home"]} : {g["score"]["away"]}</div><div class="status live">진행 중</div>'
    elif g["status"] == "FINISHED":
        right = f'<div class="score">{g["score"]["home"]} : {g["score"]["away"]}</div><div class="status done">경기 종료</div>'
    else:
        right = '<div class="status cancel">경기 취소</div>'

    return f"""
    <div class="kbo-game-card">
        <div>
            <div class="vs">{e(g["home"])} vs {e(g["away"])}</div>
            <div class="stadium">{e(g["stadium"])}</div>
        </div>
        <div class="right">{right}</div>
    </div>
    """


def render_hitter_table(team, players):
    e = html.escape
    color = team_color(team)
    rows = "".join(
        f"<tr><td>{e(p['name'])}</td>"
        f"<td style='color:{color};font-weight:600;'>{p['avg']:.3f}</td>"
        f"<td>{p['g']}</td><td>{p['h']}</td><td>{p['double']}</td>"
        f"<td>{p['triple']}</td><td>{p['hr']}</td><td>{p['rbi']}</td></tr>"
        for p in players
    )
    return f"""
    <div class="kbo-team-band" style="background:{color};">
        <span>{e(team)} 타자</span><span class="n">{len(players)}명</span>
    </div>
    <div class="kbo-table-wrap">
        <table class="kbo-table">
            <thead><tr><th>이름</th><th>타율</th><th>경기</th><th>안타</th><th>2루타</th><th>3루타</th><th>홈런</th><th>타점</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """


def render_pitcher_table(team, pitchers):
    e = html.escape
    color = team_color(team)
    rows = "".join(
        f"<tr><td>{e(p['name'])}</td>"
        f"<td style='color:{color};font-weight:600;'>{p['era']:.2f}</td>"
        f"<td>{p['g']}</td><td>{p['w']}</td><td>{p['l']}</td>"
        f"<td>{p['sv']}</td><td>{p['hld']}</td><td>{p['so']}</td><td>{p['whip']:.2f}</td></tr>"
        for p in pitchers
    )
    return f"""
    <div class="kbo-team-band" style="background:{color};">
        <span>{e(team)} 투수</span><span class="n">{len(pitchers)}명</span>
    </div>
    <div class="kbo-table-wrap">
        <table class="kbo-table">
            <thead><tr><th>이름</th><th>ERA</th><th>경기</th><th>승</th><th>패</th><th>세이브</th><th>홀드</th><th>탈삼진</th><th>WHIP</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
