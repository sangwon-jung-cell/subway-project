import cv2
import requests
import time

# 1. 설정값 정의
VIDEO_PATH = "video_sample.mp4"  # 또는 실시간 카메라인 경우 0, 1 등 입력
API_URL = "http://localhost:8000/detect"

TARGET_FPS = 3        # 초당 5프레임만 전송하도록 설정
RESIZE_WIDTH = 640     # 이미지 가로 크기를 640으로 축소
JPEG_QUALITY = 75      # JPEG 압축 화질을 75%로 조절

def process_video_optimized():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("❌ 영상을 열 수 없습니다.")
        return

    # 영상의 원래 FPS 확인 (예: 30 fps)
    source_fps = cap.get(cv2.CAP_PROP_FPS)
    if source_fps == 0: 
        source_fps = 30  # FPS를 가져오지 못할 경우 기본 30으로 가정
        
    # 몇 프레임마다 1번씩 보낼지 계산 (예: 30 / 5 = 6프레임마다 1장)
    frame_interval = max(1, int(source_fps / TARGET_FPS))

    frame_count = 0
    sent_count = 0

    # session
    with requests.Session() as session:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # 영상이 끝나면 종료

            frame_count += 1

            # 1. 프레임 솎아내기 (네트워크 부하 방지)
            if frame_count % frame_interval != 0:
                continue

            # 2. 해상도 줄이기 (비율 유지하면서 가로 640px 크기로)
            height, width = frame.shape[:2]
            aspect_ratio = height / width
            target_height = int(RESIZE_WIDTH * aspect_ratio)
            resized_frame = cv2.resize(frame, (RESIZE_WIDTH, target_height))

            # 3. 메모리 상에서 바로 JPG 압축 (용량 최소화)
            success, encoded_image = cv2.imencode(
                '.jpg', 
                resized_frame, 
                [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
            )
            if not success:
                continue

            frame_bytes = encoded_image.tobytes()


            files = {'file': (f'frame_{frame_count}.jpg', frame_bytes, 'image/jpeg')}
            data = {
                'gate': 'Gate_03',
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }

            try:
                response = session.post(API_URL, files=files, data=data, timeout=3)
                sent_count += 1
                print(f"🚀 [{frame_count}번 프레임] 전송 성공 (서버 응답: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"❌ [{frame_count}번 프레임] 전송 실패 (서버가 꺼져있거나 주소 오류): {e}")

    cap.release()
    print(f"\n✨ 전송 완료! (총 읽은 프레임: {frame_count} / 전송한 최적화 프레임: {sent_count})")

if __name__ == "__main__":
    process_video_optimized()