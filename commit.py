"""把 data/occupancy.csv 的變更 commit 並 push（Linux / Windows 都能跑）。"""
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta


def git(*args, check=True):
    return subprocess.run(["git", *args], check=check)


def main() -> int:
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("add", "data/occupancy.csv")
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("沒有新資料")
        return 0
    now = datetime.now(timezone(timedelta(hours=8)))
    git("commit", "-m", f"data: {now:%Y-%m-%d %H:%M}")
    for i in range(3):
        if git("pull", "--rebase", check=False).returncode == 0 and \
           git("push", check=False).returncode == 0:
            return 0
        time.sleep(5 * (i + 1))
    print("push 失敗", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
