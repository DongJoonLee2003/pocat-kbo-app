import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

DETAIL_URLS = {
    "hitter": "https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId={id}",
    "pitcher": "https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId={id}",
}

FIELD_SUFFIXES = {
    "photo_url": "imgProgile",
    "name": "lblName",
    "back_no": "lblBackNo",
    "birthday": "lblBirthday",
    "position": "lblPosition",
    "height_weight": "lblHeightWeight",
    "career": "lblCareer",
}


def fetch_player_detail(player_id, kind="hitter"):
    url = DETAIL_URLS[kind].format(id=player_id)
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    info = {}
    for key, suffix in FIELD_SUFFIXES.items():
        el = soup.find(id=lambda x: x and x.endswith(suffix))
        if not el:
            info[key] = None
            continue
        if key == "photo_url":
            src = el.get("src", "")
            info[key] = "https:" + src if src.startswith("//") else src
        else:
            info[key] = el.get_text(strip=True)
    return info
