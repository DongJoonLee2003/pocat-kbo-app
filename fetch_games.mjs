import path from "node:path";
import fs from "node:fs";
import { execSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const globalRoot = execSync("npm root -g").toString().trim();
const entry = pathToFileURL(path.join(globalRoot, "kbo-game", "dist", "index.js")).href;
const { getGame } = await import(entry);

const todayKST = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul" }).format(new Date());
const games = await getGame(new Date(`${todayKST}T00:00:00+09:00`));

const simplified = games.map((g) => ({
  stadium: g.stadium,
  home: g.homeTeam,
  away: g.awayTeam,
  startTime: g.startTime,
  status: g.status,
  score: { home: g.score.home, away: g.score.away },
}));

fs.writeFileSync("games.json", JSON.stringify(simplified, null, 2), "utf-8");
console.log(`saved games.json: ${simplified.length} games (${todayKST})`);
