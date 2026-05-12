from ultralytics import YOLO

# 모델 파일 경로 (컨테이너 내부 경로 기준)
model = YOLO("models/best.pt")

# 테스트 예시
# results = model.predict(source="이미지경로", save=False)