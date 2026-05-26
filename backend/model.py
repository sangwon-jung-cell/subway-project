import requests

API_URL = "http://localhost:8000/detect"
# 테스트할 이미지 경로
IMAGE_PATH = "frame.jpg" 

def send_frame_to_backend():
    try:
        with open(IMAGE_PATH, "rb") as f:
            # API의 파라미터명인 'file'과 정확히 일치시켜야 합니다.
            files = {"file": (IMAGE_PATH, f, "image/jpeg")}
            
            print("🚀 백엔드로 이미지 전송 및 분석 요청 중...")
            response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("📥 분석 결과:", result)
                
                # 부정승차가 감지되었을 때 추가 로직 처리 가능
                if result.get("status") == "intrusion_detected":
                    print(f"🚨 경보!! {result.get('event_type')} 감지됨!")
            else:
                print(f"❌ 서버 에러 발생: {response.status_code}")
                
    except Exception as e:
        print(f"🔴 연결 실패: {e}")

# 실행
if __name__ == "__main__":
    send_frame_to_backend()