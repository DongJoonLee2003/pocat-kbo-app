import json
from datetime import datetime, timedelta, timezone
import requests

URL = "https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.koreabaseball.com",
    "Referer": "https://www.koreabaseball.com/",
    "User-Agent": "Mozilla/5.0",
}

STATUS_MAP = {
    "1": "SCHEDULED",
    "2": "IN_PROGRESS",
    "3": "FINISHED",
    "4": "CANCELED",
}


def fetch_games():
    kst_today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y%m%d")
    data = {
        "leId": "1",
        "srId": "0,1,3,4,5,6,7,8,9",
        "date": kst_today,
    }
    resp = requests.post(URL, headers=HEADERS, data=data)
    resp.raise_for_status()
    games = resp.json().get("game", [])

    simplified = [
        {
            "stadium": g["S_NM"],
            "home": g["HOME_NM"],
            "away": g["AWAY_NM"],
            "startTime": g["G_TM"],
            "status": STATUS_MAP.get(g["GAME_STATE_SC"], "SCHEDULED"),
            "score": {"home": int(g["B_SCORE_CN"]), "away": int(g["T_SCORE_CN"])},
        }
        for g in games
    ]

    with open("games.json", "w", encoding="utf-8") as f:
        json.dump(simplified, f, ensure_ascii=False, indent=2)

    return simplified


if __name__ == "__main__":
    result = fetch_games()
    print(f"saved games.json: {len(result)} games")
