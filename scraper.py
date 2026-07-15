import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

URL = "https://gm-h.goebc.kr/gm-h/na/ntt/selectNttList.do?mi=6578&bbsId=1001"
CHECKED_FILE = "checked_competitions.json"

KEYWORDS = ["콘텐츠", "크리에이터", "영상", "비디오", "편집", "유튜브", "숏폼", "틱톡", "릴스", "웹툰", "애니메이션", "디자인", "대회", "경진", "페스티벌", "콘테스트", "공모", "참가신청", "접수", "모집"]

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def load_checked():
    if os.path.exists(CHECKED_FILE):
        with open(CHECKED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_checked(checked):
    with open(CHECKED_FILE, 'w', encoding='utf-8') as f:
        json.dump(checked, f, ensure_ascii=False, indent=2)

def send_to_discord(message):
    if not DISCORD_WEBHOOK:
        print("❌ DISCORD_WEBHOOK 시크릿이 등록되지 않았습니다.")
        return
    requests.post(DISCORD_WEBHOOK, json={"content": message})

def check_new_competitions():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 체크 시작")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    checked = load_checked()
    new_found = []

    for item in soup.select("td.title a, a.ntt_ttl, .tit a"):
        title = item.get_text().strip()
        if not title: continue
        link = item['href']
        if not link.startswith("http"):
            link = "https://gm-h.goebc.kr" + link

        if any(kw in title for kw in KEYWORDS) and title not in [c['title'] for c in checked]:
            new_found.append({"title": title, "link": link})
            checked.append({"title": title, "link": link})

    if new_found:
        msg = "@everyone\n\n🎉 **경기경영고 새 대회 발견!** 🎉\n\n"
        for n in new_found:
            msg += f"• {n['title']}\n  {n['link']}\n\n"
        print(msg)
        send_to_discord(msg)
        save_checked(checked)
    else:
        print("새 대회 소식 없음")

if __name__ == "__main__":
    check_new_competitions()
