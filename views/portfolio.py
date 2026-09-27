import json
import streamlit as st
import streamlit.components.v1 as components

IMG = "assets/portfolio/"


def mermaid(code, height, max_width=1100):
    # Streamlit은 mermaid를 직접 못 그려서, mermaid.js를 불러와 SVG로 그린 뒤 끼워 넣는다
    components.html(
        f"""
<div id="diagram" style="max-width:{max_width}px;margin:0 auto;"></div>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false, theme:'neutral', fontFamily:'Noto Sans KR, sans-serif'}});
const {{svg}} = await mermaid.render('g', {json.dumps(code)});
document.getElementById('diagram').innerHTML = svg;
</script>
""",
        height=height,
    )


def code_fix(title, wrong, right, lesson):
    st.markdown(f"**{title}**")
    left, right_col = st.columns(2)
    with left:
        st.caption("❌ 처음 짠 코드")
        st.code(wrong, language="python")
    with right_col:
        st.caption("✅ 고친 코드")
        st.code(right, language="python")
    st.info(lesson)


def section(num, title, date):
    st.divider()
    st.caption(date)
    st.header(f"{num}. {title}")


# ─────────────────────────────────────────────
st.title("PoCaT KBO — 포트폴리오")
st.markdown(
    "#### AI에게 코드를 통째로 받지 않고, 파이썬 기초부터 직접 짜면서 만든 KBO 기록 사이트"
)
st.write(
    "8월 22일부터 9월 27일까지, 토요일마다 작업한 과정을 날짜순으로 정리했다. "
    "잘 된 것만이 아니라 틀린 코드, 바꾼 계획, 되돌린 기능까지 그대로 적었다."
)
st.link_button("🔗 배포된 사이트 보기", "https://pocat-kbo-app-dongjoon2003.streamlit.app/")

c1, c2, c3, c4 = st.columns(4)
c1.metric("작업한 날", "5일", "8/22 ~ 9/27")
c2.metric("첫 진단 점수", "1 / 5", "파이썬 기초 5문항")
c3.metric("선수 데이터", "575명", "타자 287 + 투수 288")
c4.metric("git 커밋", "25개", "9/5 첫 커밋부터")

st.subheader("타임라인")
mermaid(
    """timeline
    8/22 1주차 : 주제 정하기 : 자가진단 5문항 중 1개 : 계획을 스탯 조회 사이트로 축소
    8/29 2주차 : Learning 모드로 문법 진단 : 리스트·딕셔너리·함수·파일 : 첫 Streamlit 화면
    9/5 3주차 : 실제 KBO 데이터 연결 : 팀 선택 필터 직접 구현 : 첫 배포
    9/19 5주차 : 배포 에러 수정 : 선수 30명에서 575명으로 : 디자인 개편
    9/27 6주차 : 포트폴리오 정리
""",
    height=400,
)

# ─────────────────────────────────────────────
section(1, "출발: 하고 싶은 것과 할 수 있는 것", "2026.08.22 · 1주차")

st.write(
    "처음 하고 싶었던 건 **승률 예측 + 경기 결과 맞히기 이벤트 + 팀별 팬 커뮤니티**였다. "
    "팀원에게서도 \"야구를 보는 사람들을 위한 커뮤니티를 만들면 좋겠다\"는 피드백을 받았다. "
    "그런데 주제를 정하면서 두 가지 현실을 확인했다."
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### ① 이미 있는 서비스")
    st.write(
        "KBO 기록은 스탯티즈와 KBO 공식 기록실이 이미 잘 하고 있다. "
        "\"선수 스탯 보여주는 사이트\"를 또 만들어서 실사용자를 모으는 건 짧은 기간에 어렵다. "
        "그래서 목표를 \"실사용자 N명\"이 아니라 **\"왜 이렇게 만들었는지 설명할 수 있는 프로젝트\"** 로 바꿨다."
    )
    st.markdown("##### ② 쓸 수 있는 시간")
    st.write(
        "5주 × 4시간 = 20시간인데, 첫날은 1시간만 남아 있어서 **실질 17시간**이었다. "
        "커뮤니티는 회원가입·글쓰기·신고까지 붙으면 그것만으로 시간을 다 쓴다. "
        "상품을 거는 이벤트는 사행성 규제에 걸릴 소지도 있었다."
    )
with col2:
    st.markdown("##### ③ 내 실력 자가진단")
    st.table(
        [
            {"문항": "리스트에서 짝수만 골라 새 리스트 만들기", "결과": "논리는 맞지만 실행 안 됨"},
            {"문항": "df[df['team'] == 'Lotte'] 의미", "결과": "모름"},
            {"문항": "KeyError: 'ERA' 대응", "결과": "방향은 맞음"},
            {"문항": "return이 없으면?", "결과": "맞음"},
            {"문항": "pandas로 두 표 합치기", "결과": "모름"},
        ]
    )
    st.write(
        "**5문항 중 1개.** ADsP 자격증이 있고 강의도 들었지만, "
        "개념을 읽기만 하고 손으로 짜본 적은 거의 없었다는 걸 알게 됐다."
    )

st.image(IMG + "01_plan_roadmap.png", width=820, caption="원래 계획에서 수정된 계획으로, 그리고 5주 로드맵")
st.success(
    "**결정:** 예측 없이 \"KBO 선수 스탯 조회 사이트\"로 줄였다. 시시해 보여도 "
    "데이터 가져오기 → 정리하기 → 화면에 보여주기 → 인터넷에 올리기가 다 들어 있고, "
    "이걸 내 손으로 끝까지 해내는 게 지금 할 수 있는 최선이라고 판단했다."
)

# ─────────────────────────────────────────────
section(2, "규칙 만들기: AI를 '조수'가 아니라 '과외 선생님'으로", "2026.08.22 · 1주차")

st.write(
    "예전에 AI에게 코드를 통째로 받아서 프로젝트를 \"완성\"한 적이 있는데, "
    "나중에 내가 뭘 했는지 하나도 설명하지 못했다. 이번엔 그걸 반복하지 않으려고 "
    "Claude Code의 출력 스타일을 **Learning 모드**로 바꾸고, 세션을 시작할 때 쓸 규칙 프롬프트를 직접 만들었다."
)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("##### 과외 선생님 규칙 7가지")
    st.markdown(
        """
1. **완성된 코드를 먼저 주지 마라** — 설명 → 순서 안내 → "직접 짜봐" → 피드백
2. **한 번에 한 걸음만**
3. **모르는 용어는 일상 비유로** (예: "함수는 자판기")
4. **매 단계마다 질문으로 시험**
5. **결과물을 빨리, 자주 보여줄 것**
6. **솔직하게** — 코드가 별로면 별로라고
7. **세션 끝에 진도 기록** — 한 것 / 배운 것 / 모르는 것 / 다음 할 것
"""
    )
with col2:
    st.markdown("##### 프롬프트를 한 번 고친 이유")
    st.write(
        "첫 버전 프롬프트에는 \"나는 for문을 못 쓴다, pandas를 모른다\"처럼 내 실력을 미리 적어 넣었다. "
        "그런데 이렇게 하면 AI가 내 실제 코드 대신 **내가 한 말**로 수준을 정해버린다. "
        "그래서 두 번째 버전에서는 \"이력만으로 실력을 판단하지 말고, "
        "첫 세션에 직접 문제를 내서 진단하라\"로 바꿨다."
    )

st.markdown("##### 강사님 피드백을 반영해 바꾼 기술 선택")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**pandas → 순수 파이썬**")
    st.write(
        "pandas는 필터링·정렬을 다 알아서 해주는 도구다. for문과 리스트도 손에 안 붙은 상태에서 "
        "바로 pandas로 가면 \"라이브러리가 해준 것\"과 \"내가 이해한 것\"의 경계가 흐려진다. "
        "그래서 딕셔너리 리스트와 json 모듈만으로 직접 걸러내고 정리하기로 했다."
    )
with col2:
    st.markdown("**크롤링 → browser-use (계획)**")
    st.write(
        "데이터 수집은 LLM이 브라우저를 직접 조작하는 browser-use를 쓰기로 했다. "
        "다만 호출할 때마다 비용이 들기 때문에 **한 번 가져온 결과는 바로 파일로 저장하고, "
        "화면 작업은 저장된 파일로만 한다**는 원칙을 같이 정했다. (이 계획은 3주차에 바뀐다 → 4번 항목)"
    )

# ─────────────────────────────────────────────
section(3, "문법 점검: 직접 짜고, 틀리고, 고치기", "2026.08.22 ~ 08.29 · 1~2주차")

st.write(
    "Learning 모드의 첫 작업은 진단이었다. AI가 문제를 내면 **아무것도 보지 않고 직접** 짜고, "
    "틀리면 정답 대신 질문을 받아서 내가 원인을 찾았다. 같은 짝수 문제를 세 번에 걸쳐 푼 과정이 가장 잘 보여준다."
)

st.markdown("##### 짝수 고르기 — 같은 문제를 세 번")
a, b, c = st.columns(3)
with a:
    st.caption("8/22 첫 시도 (자가진단)")
    st.code(
        """for i in List[i]:
    if List[i] % 2 == 0:
        New_List = List[i]
    else:
        pass;""",
        language="python",
    )
    st.write("리스트가 아니라 `List[i]`를 돌고, 결과를 덮어써서 마지막 값 하나만 남는다. 빈 리스트도 안 만들었다.")
with b:
    st.caption("8/22 두 번째 (Learning 모드)")
    st.code(
        """new_list = []
for i in list:
    if (list[i] % 2) == 0:
        new_list += list[i]
    else:
        pass;""",
        language="python",
    )
    st.write("빈 리스트를 먼저 만든 건 고쳐졌다. 하지만 `i`는 **순번이 아니라 값**이라서 `list[i]`가 엉뚱한 칸을 가리킨다.")
with c:
    st.caption("8/29 완성")
    st.code(
        """new_list = []
for i in numbers:
    if i % 2 == 0:
        new_list.append(i)""",
        language="python",
    )
    st.write("`print(i)`로 직접 찍어보고 값이라는 걸 확인했다. `+=`에서 난 `TypeError`를 보고 \"자료형 문제 같다\"고 먼저 짚은 뒤 `append`로 바꿨다.")

code_fix(
    "딕셔너리 — 점(.)이 아니라 대괄호",
    """# 처음엔 for문 없이 점으로 접근하려 했다
players_team.value

# 두 번째: = 와 == 혼동, 콜론 누락
for i in players:
    if (i["team"] ="LG")""",
    """for i in players:
    if i["team"] == "LG":
        new_list.append(i["name"])
# ['김선수', '박선수']""",
    "`=`(값 넣기)와 `==`(같은지 비교)는 조건문 안이라서 비슷한 게 아니라, 원래 완전히 다른 기호라는 걸 배웠다.",
)

code_fix(
    "파일 저장/읽기 — 에러 3개를 차례로 만남",
    """json.dump(players = [...], players.json)
# SyntaxError

with open("players.json", "w") as f:
    json.load(f)
# UnsupportedOperation: not readable

json.load(f)
print(json.load(f))
# JSONDecodeError""",
    """with open("players.json", "w", encoding="utf-8") as f:
    json.dump(players, f)

with open("players.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data)""",
    "쓰기(w)와 읽기(r)는 다른 모드라서 나눠서 열어야 한다. 파일은 책갈피처럼 한 번 읽으면 끝으로 가기 때문에 결과를 변수에 한 번만 담는다.",
)

col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("##### 함수 — 매개변수와 return")
    st.write(
        "`get_grade(avg)`를 만들면서 받은 `avg`는 쓰지 않고 함수 밖의 `players` 리스트를 다시 돌렸다. "
        "직전 문제가 딕셔너리였어서 이번에도 그렇게 해야 하는 줄 알았다. "
        "**함수 안에서는 넘겨받은 매개변수만으로 판단한다**는 것, 그리고 "
        "`return`은 결과를 돌려주는 것이고 `print`는 화면에 보여주는 것이라는 차이를 이때 알았다."
    )
    st.markdown("##### 그리고 첫 화면")
    st.write(
        "진단에서 배운 딕셔너리·for문·json을 그대로 조합해서 Streamlit에 선수 3명을 띄웠다. "
        "`import streamlit as st`의 별명 문법도, Streamlit이 새로고침마다 스크립트를 "
        "처음부터 다시 실행한다는 것도 이때 배웠다."
    )
with col2:
    st.image(IMG + "02_first_player_list.png", caption="8/29 처음 브라우저에 띄운 화면 — 직접 적은 선수 3명")

# ─────────────────────────────────────────────
section(4, "실제 데이터 붙이기: 배운 문법을 조합하기", "2026.09.05 · 3주차")

st.write(
    "\"오늘 KBO 경기 결과가 궁금하다\"는 질문에서 시작해서, 그 결과를 실제로 사이트에 띄우는 데까지 갔다. "
    "데이터를 **가져오는 스크립트**는 학습 목표가 아니라서 Claude가 짰고, "
    "가져온 파일을 **읽어서 걸러내고 보여주는 부분**은 내가 직접 짰다."
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 내가 직접 짠 코드 (3주차 app.py 그대로)")
    st.code(
        """with open("hitters.json","r", encoding="utf-8") as f:
    hitters = json.load(f)
    team_names = []
    for i in hitters:
        if i["team"] not in team_names:
            team_names.append(i["team"])
    selected_team = st.radio("팀을 선택하세요", team_names)
    for player in hitters:
        if player["team"] == selected_team:
            st.write(f"{player['name']} / {player['team']} / {player['avg']}")""",
        language="python",
    )
    st.write(
        "- **중복 없는 팀 목록**: `not in`으로 직접 구현했다. 보너스로 안내받은 방법이었는데 힌트 없이 첫 시도에 성공했다.\n"
        "- **필터링**: 2주차 딕셔너리 문제의 `\"LG\"` 자리에 화면에서 고른 팀이 들어가는 응용이다.\n"
        "- **경기 상태 분기**: 2갈래로 안내받았지만 예정·진행중·종료·취소 4갈래로 나눴다."
    )
with col2:
    st.markdown("##### 이번 주에 새로 만난 것")
    st.write(
        "- **중첩 딕셔너리**: `game[\"score\"][\"home\"]`처럼 대괄호를 두 번 쓴다.\n"
        "- **f-string**: 중괄호를 빼먹으면 변수 대신 글자가 그대로 나온다.\n"
        "- **인코딩**: `games.json`을 열다가 `UnicodeDecodeError: 'cp949'`가 났다. "
        "2주차에 배운 `encoding=\"utf-8\"`을 빠뜨린 것이었다. 그 뒤 `hitters.json`을 열 때는 힌트 없이 처음부터 넣었다."
    )
    st.warning(
        "**반복된 실수:** `json.load()`, `st.radio()`처럼 **값을 돌려주는 함수**의 결과를 변수에 담지 않고 쓰려는 실수를 "
        "한 세션에 세 번 했다. 지적받으면 바로 고쳤지만, 새 함수를 만날 때마다 다시 나왔다."
    )

b1, b2 = st.columns(2)
b1.image(IMG + "03_players_and_games.png", caption="연습용 선수 3명 아래에 오늘 경기와 팀 선택을 붙인 화면")
b2.image(IMG + "04_games_team_radio.png", caption="실제 KBO 경기 목록 + 팀을 고르면 그 팀 선수만 보이는 필터")

st.markdown("##### 데이터를 어디서 가져올지 — 계획과 달라진 것")
st.write(
    "- **browser-use를 못 썼다.** 작업 환경에 그 도구 자체가 연결돼 있지 않았다. "
    "조용히 다른 방법으로 넘어가지 않고, `requests + BeautifulSoup`으로 KBO 공식 사이트를 직접 읽는 방식으로 바꿀지 먼저 상의한 뒤 결정했다.\n"
    "- **경기 결과는 `kbo-game`이라는 공개 패키지**를 썼다.\n"
    "- **robots.txt 확인**: KBO 공식 사이트는 사전 승인 없는 자동 수집을 막고 있다. 대안으로 본 스탯티즈는 AI 봇을 명시적으로 차단해서 제외했다. "
    "공식 공개 API도 없어서, 위험을 알고 **작은 개인·교육용 프로젝트**로 범위를 한정하기로 했다."
)

# ─────────────────────────────────────────────
section(5, "배포하고 나서 만난 에러들", "2026.09.05 ~ 09.19 · 3~5주차")

st.write(
    "9월 5일 GitHub에 올리고 Streamlit Community Cloud로 배포했다. 처음엔 Vercel을 생각했지만, "
    "Streamlit은 서버가 계속 켜져 있어야 하는 구조라 맞지 않았다. 배포는 끝이 아니라 새 에러의 시작이었다."
)

col1, col2 = st.columns([3, 2])
with col1:
    st.image(IMG + "06_deploy_node_error.png", caption="배포된 사이트에서 새로고침을 누르자 난 FileNotFoundError")
with col2:
    st.markdown("##### ① 새로고침이 배포 사이트에서만 안 됨")
    st.write(
        "내 컴퓨터에서는 잘 되던 새로고침 버튼이 배포 사이트에서는 에러를 냈다. "
        "Traceback을 보면 `subprocess.run([\"node\", ...])`에서 멈춘다. "
        "새로고침이 Node.js 스크립트를 실행하는데, **배포 서버에는 Node.js가 없었다.**"
    )
    st.write(
        "`kbo-game` 패키지를 열어보니 결국 KBO 사이트 주소 하나에 요청 한 번을 보내는 게 전부였다. "
        "그래서 같은 요청을 파이썬 `requests`로 다시 만들었다(`fetch_games.py`). "
        "다른 프로그램을 부르는 `subprocess`가 필요 없어져서 코드도 더 단순해졌다."
    )

st.markdown("##### ② 선수 30명 → 575명")
st.write(
    "3주차엔 타율 상위 30명만 가져올 수 있었다. KBO 기록 페이지는 2페이지부터 링크가 아니라 "
    "페이지 전체를 다시 보내는 방식(ASP.NET postback)이라 넘기기가 까다로웠다. "
    "지난번엔 페이지가 숨겨서 들고 있는 값 중 3개만 보내서 실패했다는 걸 확인했고, "
    "**전체 목록을 넘기는 대신 팀 드롭다운으로 10개 팀을 하나씩 요청**하는 방식으로 바꿨다. "
    "결과는 타자 287명, 같은 방식으로 투수 288명까지 모았다."
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### ③ HTML이 그림 대신 글자로 보임")
    st.write(
        "경기 카드 HTML이 화면에 코드 그대로 찍혔다. 들여쓰기 때문에 마크다운이 코드블록으로 인식한 것이었는데, "
        "들여쓰기만 고쳤더니 **HTML 안의 빈 줄** 때문에 또 끊겼다. 원인을 한 번에 못 찾아 두 번 고쳤다."
    )
with col2:
    st.markdown("##### ④ 되돌린 기능과 겹친 색")
    st.write(
        "타율 막대그래프는 만들어서 배포까지 했지만 결과물이 마음에 들지 않아 **되돌렸다.** "
        "팀 색을 입힐 때는 KT와 KIA가 같은 빨간 계열이라 구분이 안 돼서 KT를 검정으로 바꿨다."
    )

# ─────────────────────────────────────────────
section(6, "디자인 전후: 한 페이지 → 화면별 분리", "2026.09.19 · 5주차")

st.write(
    "기능이 늘면서 모든 게 한 페이지에 세로로 쌓여 있었다. 기능마다 화면을 나누고 디자인도 바꾸고 싶었는데, "
    "말로만 \"예쁘게\"라고 하면 결과를 고를 기준이 없다. 그래서 **같은 데이터로 시안 4개를 만들어 달라고 해서** 비교한 뒤 골랐다."
)
st.image(IMG + "05_design_four_options.png", caption="같은 데이터, 네 가지 방향 — A 카드형 / B 표 / C 탭+강조카드 / D 팀컬러")
st.write(
    "경기는 숫자를 크게 보여주는 **카드형(A)**, 선수 기록은 여러 명을 한눈에 비교하는 **표(B)** 에 **팀 색(D)** 을 입히는 조합으로 정했다."
)

st.markdown("##### Before → After")
b, a = st.columns(2)
with b:
    st.caption("BEFORE · 9/5 — 텍스트 한 줄씩")
    st.image(IMG + "04_games_team_radio.png")
with a:
    st.caption("AFTER · 9/19 — 경기 카드")
    st.image(IMG + "after_games.png")

b, a = st.columns(2)
with b:
    st.caption("BEFORE · 8/29 — 직접 적은 3명")
    st.image(IMG + "02_first_player_list.png")
with a:
    st.caption("AFTER · 9/19 — 팀 색을 입힌 표, 팀당 24~34명")
    st.image(IMG + "after_stats.png")

st.image(IMG + "after_home.png", caption="AFTER — 홈 화면과 상단 탭으로 화면 분리")

# ─────────────────────────────────────────────
section(7, "이 사이트는 어떻게 돌아가나", "현재 구조")

st.write(
    "처음 정한 원칙인 **\"가져온 데이터는 바로 파일로 저장하고, 화면은 파일만 읽는다\"** 가 끝까지 구조의 뼈대가 됐다. "
    "화면을 열 때마다 KBO 사이트에 요청하지 않기 때문에 빠르고, 요청 수도 적다."
)
mermaid(
    """flowchart LR
    subgraph KBO["koreabaseball.com"]
        API["경기 목록<br/>GetKboGameList"]
        REC["선수 기록 페이지<br/>ASP.NET postback"]
        DET["선수 상세 페이지"]
    end
    subgraph PY["수집 스크립트 · requests + BeautifulSoup"]
        FG["fetch_games.py"]
        FH["fetch_hitters.py<br/>fetch_pitchers.py<br/>팀별 요청 + 페이지 넘기기"]
        PD["player_detail.py<br/>고른 선수 1명만"]
    end
    subgraph FILE["저장된 파일"]
        GJ["games.json"]
        HJ["hitters.json · 287명"]
        PJ["pitchers.json · 288명"]
    end
    subgraph APP["Streamlit 화면"]
        V0["홈"]
        V1["오늘 KBO 경기"]
        V2["팀별 선수 기록"]
        V3["선수 정보"]
    end
    API --> FG --> GJ
    REC --> FH --> HJ
    FH --> PJ
    GJ --> V0
    GJ --> V1
    PJ --> V1
    HJ --> V2
    PJ --> V2
    HJ --> V3
    PJ --> V3
    DET --> PD --> V3
    V1 -. "새로고침 버튼" .-> FG
""",
    height=560,
    max_width=820,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**경기 결과 — 버튼으로 갱신**")
    st.write("새로고침을 누르면 `fetch_games()`가 오늘 경기를 다시 받아 `games.json`을 덮어쓰고 화면을 다시 그린다.")
with col2:
    st.markdown("**선수 기록 — 내가 갱신**")
    st.write("타자·투수 수집은 요청이 수십 번이라 버튼에 달지 않았다. 내 컴퓨터에서 실행 → GitHub에 올리면 배포 사이트가 자동으로 다시 뜬다.")
with col3:
    st.markdown("**선수 사진 — 필요할 때만**")
    st.write("575명 상세 정보를 미리 다 긁지 않고, 화면에서 **고른 선수 1명만** 그때 가져온다.")

st.markdown("##### 새로고침 버튼을 누르면")
mermaid(
    """sequenceDiagram
    actor U as 사용자
    participant S as today_games.py
    participant F as fetch_games()
    participant K as koreabaseball.com
    participant J as games.json
    U->>S: 새로고침 클릭
    S->>F: 함수 호출
    F->>K: POST 오늘 날짜 경기 목록
    K-->>F: 경기 JSON
    F->>J: 필요한 값만 골라 덮어쓰기
    S->>S: st.rerun() 처음부터 다시 실행
    S->>J: 파일 읽기
    S-->>U: 경기 카드 표시
""",
    height=620,
    max_width=900,
)

# ─────────────────────────────────────────────
section(8, "AI를 어떻게 썼나 — 솔직하게", "8/22 ~ 9/27 전체")

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 내가 직접 짠 것 (1~3주차)")
    st.write(
        "- 문법 진단 4영역(리스트·딕셔너리·함수·파일)\n"
        "- 첫 Streamlit 화면\n"
        "- 경기 상태 4갈래 분기, 중복 없는 팀 목록, 팀 선택 필터\n\n"
        "이 구간은 Learning 모드 규칙대로 \"직접 짜봐 → 틀린 곳을 질문으로 짚기 → 내가 고치기\"로 진행했다."
    )
with col2:
    st.markdown("##### AI에게 맡긴 것")
    st.write(
        "- 데이터 수집 스크립트 전부 (처음부터 학습 목표가 아니었음)\n"
        "- 배포 설정, Node → Python 전환\n"
        "- 9/19 세션의 스탯 확장·투수 기록·디자인 개편\n\n"
        "9/19에는 시간이 부족해서 예외적으로 AI가 직접 구현하게 했다."
    )
st.warning(
    "**아직 못 한 것:** 원래 계획에 있던 \"정렬을 순수 파이썬으로 직접 짜보기\"는 두 세션 연속 시간이 부족해서 손대지 못했다. "
    "9/19 이후 추가된 코드는 내가 읽고 설명할 수는 있지만 직접 짠 것은 아니다. 이 부분을 직접 다시 짜보는 게 다음 과제다."
)
st.write(
    "AI가 틀린 것도 있었다. 선수 기록을 가져올 때 보낼 값을 빠뜨린 것, HTML이 글자로 보이던 것, "
    "두 팀의 색을 같은 계열로 정한 것. 셋 다 결과를 직접 켜보고 이상하다고 짚은 뒤에야 고쳐졌다. "
    "\"AI가 짜준 코드가 안 돌아갈 때 어디가 문제인지 읽을 수 있어야 한다\"는 처음 규칙이 여기서 쓸모 있었다."
)

# ─────────────────────────────────────────────
section(9, "6주 전의 나와 달라진 점", "2026.09.27 · 6주차")

st.write("이전의 나는 파이썬 문법을 읽기만 하고 직접 짜본 적이 거의 없었다. 지금은 딕셔너리·for문·함수·파일 입출력까지 직접 짜고, 틀린 곳을 찾아 고칠 수 있다. Streamlit 화면도 직접 만들고 배포까지 해봤다. AI를 조수로 쓰되, 내가 직접 코드를 이해하고 설명할 수 있는 수준까지 끌어올렸다.")

# ─────────────────────────────────────────────
section(10, "다음에 할 것", "이후 계획")

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 화면 톤 맞추기")
    st.write(
        "오늘 경기 화면은 어두운 카드, 팀별 기록은 흰 배경이라 탭을 넘길 때마다 다른 사이트처럼 느껴진다. "
        "전체 색을 다시 짜야 해서 이번엔 손대지 않았다. 버튼·선택창 같은 기본 구성요소까지 같은 톤으로 맞출 계획이다."
    )
    st.markdown("##### 정렬 직접 짜기")
    st.write("타율 높은 순, 홈런 많은 순 정렬을 `sorted()`와 `key`로 직접 구현해서 표에 붙인다.")
with col2:
    st.markdown("##### 처음 하고 싶었던 것으로 돌아가기")
    st.write(
        "KBO를 좋아하는 사람들이 쓰는 사이트인 만큼, 서로 이야기를 나눌 수 있는 **커뮤니티**와 "
        "지금까지 모은 경기·선수 데이터를 활용한 **승률 예측 모델**을 넣고 싶다. "
        "1주차에 \"지금 실력으로는 무리\"라며 미뤘던 기능이다. "
        "다만 이 프로젝트는 예측 모델을 쓰지 않는 조건으로 시작했기 때문에, 만들려면 그 조건부터 다시 정해야 한다."
    )
