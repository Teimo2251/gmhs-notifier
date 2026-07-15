import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# 학교 공지사항 URL (알림마당 공지사항 페이지 URL로 바꿔주세요)
URL = "https://gm-h.goebc.kr/gm-h/na/ntt/selectNttList.do?mi=6578&bbsId=1001"  # ← 이 부분 확인 필요

CHECKED_FILE = "checked_competitions.json"
KEYWORDS = ["대회", "경진", "경시", "페스티벌", "콘테스트", "공모", "참가신청", "접수", "모집", "상업경진", "뷰티", "요리대회"]

def load_checked():
    if os.path.exists(CHECKED_FILE):
        with open(CHECKED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_checked(checked):
    with open(CHECKED_FILE, 'w', encoding='utf-8') as f:
        json.dump(checked, f, ensure_ascii=False, indent=2)

def check_new_competitions():
    print(f"[{datetime.now()}] 체크 시작...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    checked = load_checked()
    new_found = []
    
    # 공지 제목들 추출 (사이트 구조에 따라 아래 selector 수정 필요)
    for item in soup.select("a.ntt_ttl"):   # ← F12 눌러서 실제 클래스 확인해서 수정
        title = item.get_text().strip()
        link = "https://gm-h.goebc.kr" + item['href'] if item['href'].startswith('/') else item['href']
        
        if any(kw in title for kw in KEYWORDS) and title not in [c['title'] for c in checked]:
            new_found.append({"title": title, "link": link, "date": str(datetime.now().date())})
            checked.append({"title": title, "link": link})
    
    if new_found:
        print(f"🔔 {len(new_found)}개의 새 대회 발견!")
        for item in new_found:
            print(f"• {item['title']}")
            print(f"  🔗 {item['link']}\n")
        
        # 여기서 Telegram 보내는 코드 추가 가능
        save_checked(checked)
    else:
        print("새 대회 소식 없음")

if __name__ == "__main__":
    check_new_competitions()
