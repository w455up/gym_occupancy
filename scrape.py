"""抓取淡水國民運動中心首頁的即時人數，追加到 data/occupancy.csv。

只用 Python 標準庫，GitHub Actions 上不用安裝任何套件。
"""
import csv
import html
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://wstssc.com.tw/"
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "occupancy.csv")
TPE = timezone(timedelta(hours=8))
FIELDS = ["timestamp_tpe", "gym", "gym_max", "pool", "pool_max"]


def fetch(url: str, retries: int = 3) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.9",
    })
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"無法取得 {url}: {last}")


def to_text(page: str) -> str:
    page = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    return re.sub(r"\s+", " ", html.unescape(page))


def parse(page: str) -> dict:
    text = to_text(page)

    def grab(name: str):
        # 網頁上同時有「32 人 容留150人」與「32 人/150人」兩種寫法
        m = re.search(name + r"\s*(\d+)\s*人\s*(?:/|容留)\s*(\d+)\s*人", text)
        return (int(m.group(1)), int(m.group(2))) if m else (None, None)

    gym, gym_max = grab("健身房")
    pool, pool_max = grab("游泳池")
    if gym is None:
        raise ValueError("頁面上找不到健身房人數，網站格式可能改了")
    return {"gym": gym, "gym_max": gym_max, "pool": pool, "pool_max": pool_max}


def append(row: dict) -> None:
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    new = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def main() -> int:
    now = datetime.now(TPE)
    # 營業時間 06:00–22:00 以外不記錄（關館時一定是 0，只會汙染平均）
    if not (6 <= now.hour < 22) and "--force" not in sys.argv:
        print(f"{now:%H:%M} 非營業時間，略過")
        return 0
    data = parse(fetch(URL))
    row = {"timestamp_tpe": now.strftime("%Y-%m-%d %H:%M"), **data}
    append(row)
    print(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
