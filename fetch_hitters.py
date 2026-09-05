import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.koreabaseball.com/record/player/hitterbasic/basic1.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(URL, headers=HEADERS)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

table = soup.find_all("table")[0]
rows = table.find_all("tr")
header = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]

players = []
for row in rows[1:]:
    cells = [td.get_text(strip=True) for td in row.find_all("td")]
    if len(cells) != len(header):
        continue
    record = dict(zip(header, cells))
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

print(f"{len(players)} players saved")

with open("hitters.json", "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=2)
