import re
import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.koreabaseball.com/record/player/hitterbasic/basic1.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0"}
TEAM_FIELD = "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlTeam$ddlTeam"

TEAM_CODES = ["KT", "SS", "LG", "HT", "OB", "NC", "LT", "SK", "HH", "WO"]


def capture_form_state(soup):
    form_data = {}
    for inp in soup.find_all("input"):
        name = inp.get("name")
        if name:
            form_data[name] = inp.get("value", "")
    for sel in soup.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        selected = sel.find("option", selected=True)
        if selected:
            form_data[name] = selected.get("value", "")
        else:
            first = sel.find("option")
            form_data[name] = first.get("value", "") if first else ""
    return form_data


def parse_players(soup):
    tables = soup.find_all("table")
    if not tables:
        return []
    rows = tables[0].find_all("tr")
    header = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]
    players = []
    for row in rows[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cells) != len(header):
            continue
        record = dict(zip(header, cells))
        if not record.get("AVG") or record["AVG"] == "-":
            continue
        players.append(
            {
                "name": record["선수명"],
                "team": record["팀명"],
                "avg": float(record["AVG"]),
                "g": int(record["G"]),
                "hr": int(record["HR"]),
                "rbi": int(record["RBI"]),
            }
        )
    return players


def next_page_target(soup, current_page):
    wanted_id_suffix = f"btnNo{current_page + 1}"
    btn = soup.find("a", id=lambda x: x and x.endswith(wanted_id_suffix))
    if not btn:
        return None
    m = re.search(r"__doPostBack\('([^']+)'", btn.get("href", ""))
    return m.group(1) if m else None


session = requests.Session()
resp = session.get(URL, headers=HEADERS)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")
base_form = capture_form_state(soup)

all_players = []
counts = {}

for code in TEAM_CODES:
    form_data = dict(base_form)
    form_data["__EVENTTARGET"] = TEAM_FIELD
    form_data["__EVENTARGUMENT"] = ""
    form_data[TEAM_FIELD] = code
    resp2 = session.post(URL, headers=HEADERS, data=form_data)
    resp2.encoding = "utf-8"
    soup2 = BeautifulSoup(resp2.text, "html.parser")

    team_players = parse_players(soup2)
    page = 1

    while True:
        target = next_page_target(soup2, page)
        if not target:
            break
        page_form = capture_form_state(soup2)
        page_form["__EVENTTARGET"] = target
        page_form["__EVENTARGUMENT"] = ""
        resp3 = session.post(URL, headers=HEADERS, data=page_form)
        resp3.encoding = "utf-8"
        soup2 = BeautifulSoup(resp3.text, "html.parser")
        team_players.extend(parse_players(soup2))
        page += 1

    seen_in_team = set()
    deduped = []
    for p in team_players:
        key = (p["name"], p["team"])
        if key in seen_in_team:
            continue
        seen_in_team.add(key)
        deduped.append(p)

    counts[code] = len(deduped)
    all_players.extend(deduped)

with open("hitters.json", "w", encoding="utf-8") as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

with open("_fetch_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"total players: {len(all_players)}\n")
    for code, cnt in counts.items():
        f.write(f"{code}: {cnt}\n")
