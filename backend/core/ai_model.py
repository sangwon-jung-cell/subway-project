from ultralytics import YOLO
import os

MODEL_PATH = "model/best.pt"
# 전역 변수로 선언하여 어디서든 불러올 수 있게 함
yolo_model = YOLO(MODEL_PATH) if os.path.exists(MODEL_PATH) else None