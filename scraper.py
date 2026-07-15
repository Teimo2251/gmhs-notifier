import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send_to_discord(message):
    if not DISCORD_WEBHOOK:
        print("❌ DISCORD_WEBHOOK 시크릿이 없습니다!")
        return
    response = requests.post(DISCORD_WEBHOOK, json={"content": message})
    print(f"디스코드 전송 결과: {response.status_code}")

if __name__ == "__main__":
    print(f"[{datetime.now()}] 테스트 시작")
    
    test_msg = "@everyone\n\n🧪 **디스코드 테스트 메시지입니다!**\n\n웹훅이 정상적으로 작동하는지 확인 중..."
    
    send_to_discord(test_msg)
    print("테스트 완료")
