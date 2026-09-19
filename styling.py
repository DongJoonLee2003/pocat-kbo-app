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

/* ── 홈 히어로: 야간 경기장 ───────────────────────── */
.kbo-hero{
    position:relative; width:100%; aspect-ratio:1000/320; max-height:340px;
    border-radius:16px; overflow:hidden; margin-bottom:8px;
    box-shadow:0 10px 30px rgba(5,20,12,.35);
}
.kbo-hero svg{position:absolute; inset:0; width:100%; height:100%; display:block;}
.kbo-hero .hero-overlay{
    position:absolute; inset:0; display:flex; flex-direction:column; justify-content:space-between;
    padding:22px 26px; font-family:'Noto Sans KR',sans-serif; color:#fff;
    pointer-events:none;
}
.kbo-hero .hero-top{display:flex; justify-content:space-between; align-items:flex-start;}
.kbo-hero .hero-date{font-size:12px; color:#bfe6d1; letter-spacing:.03em;}
.kbo-hero .hero-live{
    display:flex; align-items:center; gap:6px; font-size:12px; font-weight:700;
    background:rgba(255,255,255,.12); backdrop-filter:blur(2px);
    padding:5px 10px; border-radius:999px; color:#ffe1d6;
}
.kbo-hero .hero-live .dot{width:8px; height:8px; border-radius:50%; background:#ff5a4e;}
.kbo-hero .hero-title{font-family:'Oswald',sans-serif; font-weight:700; font-size:clamp(28px,5vw,46px); letter-spacing:.01em; text-shadow:0 2px 18px rgba(0,0,0,.45);}
.kbo-hero .hero-tag{font-size:13px; color:#cfe9da; margin-top:4px;}

@media (prefers-reduced-motion: no-preference){
    .kbo-hero .light-glow{animation:kboGlow 2.6s ease-in-out infinite;}
    .kbo-hero .flyball{animation:kboFly 6s ease-in-out infinite;}
    .kbo-hero .hero-live .dot{animation:kboPulse 1.4s ease-in-out infinite;}
}
@keyframes kboGlow{0%,100%{opacity:.55;} 50%{opacity:1;}}
@keyframes kboPulse{0%,100%{opacity:1; transform:scale(1);} 50%{opacity:.4; transform:scale(1.3);}}
@keyframes kboFly{
    0%{transform:translate(0px,0px) rotate(0deg);}
    45%{transform:translate(-330px,-165px) rotate(240deg);}
    55%{transform:translate(-330px,-165px) rotate(240deg);}
    100%{transform:translate(0px,0px) rotate(480deg);}
}
</style>
"""


def team_color(team):
    return TEAM_COLORS.get(team, DEFAULT_ACCENT)


def render_stadium_hero(today_label, total_games, live_games):
    e = html.escape

    if live_games > 0:
        live_badge = f'<div class="hero-live"><span class="dot"></span>{live_games}경기 진행 중</div>'
    else:
        live_badge = f'<div class="hero-live" style="background:rgba(255,255,255,.08);color:#dff2e6;"><span style="width:8px;"></span>오늘 {total_games}경기</div>'

    return f"""
    <div class="kbo-hero">
        <svg viewBox="0 0 1000 320" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#04140c"/>
                    <stop offset="55%" stop-color="#0a3320"/>
                    <stop offset="100%" stop-color="#164a2a"/>
                </linearGradient>
                <radialGradient id="lightGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#fff6d8" stop-opacity="0.85"/>
                    <stop offset="100%" stop-color="#fff6d8" stop-opacity="0"/>
                </radialGradient>
            </defs>

            <rect x="0" y="0" width="1000" height="320" fill="url(#skyGrad)"/>

            <circle class="light-glow" cx="70" cy="55" r="90" fill="url(#lightGlow)"/>
            <circle class="light-glow" cx="930" cy="55" r="90" fill="url(#lightGlow)"/>

            <g stroke="#dff2e6" stroke-width="2" opacity="0.5">
                <line x1="500" y1="278" x2="50" y2="28"/>
                <line x1="500" y1="278" x2="950" y2="28"/>
            </g>

            <g opacity="0.9">
                <rect x="66" y="18" width="8" height="42" fill="#0c2415"/>
                <rect x="926" y="18" width="8" height="42" fill="#0c2415"/>
                <g fill="#fff6d8">
                    <circle cx="55" cy="18" r="4"/><circle cx="70" cy="12" r="4"/><circle cx="85" cy="18" r="4"/>
                    <circle cx="915" cy="18" r="4"/><circle cx="930" cy="12" r="4"/><circle cx="945" cy="18" r="4"/>
                </g>
            </g>

            <polygon points="500,305 270,197 500,62 730,197" fill="#b5793f" opacity="0.9"/>

            <polygon points="500,275 330,195 500,95 670,195" fill="none" stroke="#f4f0e4" stroke-width="2" opacity="0.75"/>
            <circle cx="500" cy="225" r="13" fill="#b5793f"/>
            <rect x="494" y="221" width="12" height="6" fill="#f4f0e4"/>
            <rect x="493" y="271" width="14" height="10" fill="#f4f0e4" transform="rotate(45 500 275)"/>
            <rect x="323" y="188" width="14" height="14" fill="#f4f0e4" transform="rotate(45 330 195)"/>
            <rect x="493" y="88" width="14" height="14" fill="#f4f0e4" transform="rotate(45 500 95)"/>
            <rect x="663" y="188" width="14" height="14" fill="#f4f0e4" transform="rotate(45 670 195)"/>

            <g class="flyball" style="transform-origin:500px 260px;">
                <circle cx="500" cy="260" r="7" fill="#fdfaf1"/>
                <path d="M495,256 Q500,260 495,264" stroke="#c1443a" stroke-width="1" fill="none"/>
                <path d="M505,256 Q500,260 505,264" stroke="#c1443a" stroke-width="1" fill="none"/>
            </g>
        </svg>
        <div class="hero-overlay">
            <div class="hero-top">
                <div class="hero-date">{e(today_label)}</div>
                {live_badge}
            </div>
            <div>
                <div class="hero-title">PoCaT KBO</div>
                <div class="hero-tag">오늘 경기와 팀별 선수 기록을 한눈에</div>
            </div>
        </div>
    </div>
    """.strip()


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
    """.strip()


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
    """.strip()


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
    """.strip()
