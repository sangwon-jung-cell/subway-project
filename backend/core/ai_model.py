import os
from ultralytics import YOLO

MODEL_PATH = "model/best.pt"

# 로컬에 우리 팀의 best.pt가 있으면 그걸 쓰고, 없으면 YOLO 기본 경량 모델(yolov8n.pt)을 자동으로 내려받아 사용!
if os.path.exists(MODEL_PATH):
    yolo_model = YOLO(MODEL_PATH)
    print("🎯 커스텀 'best.pt' 모델 로드 완료")
else:
    yolo_model = YOLO("yolov8n.pt")
    print("🌐 'best.pt'가 없어 YOLOv8 기본 경량 모델을 자동으로 로드합니다.")