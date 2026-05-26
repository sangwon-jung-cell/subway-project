from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db, Detection_table
from manager import manager
from core.ai_model import yolo_model  # 학습된 모델 가져오기
import os
import uuid

router = APIRouter()

@router.post("")
async def detect_and_notify(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if yolo_model is None:
        return {"status": "error", "message": "YOLO 모델이 로드되지 않았습니다."}

    # [안전장치] static 폴더가 없으면 자동으로 생성해 줍니다.
    os.makedirs("static", exist_ok=True)

    # 1. 프론트/CCTV가 보낸 이미지를 임시 혹은 static에 물리 파일로 저장
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    save_path = os.path.join("static", unique_filename)

    # save_path가 윈도우에서 'static\\file.jpg'로 잡히더라도 웹 주소용인 슬래시('/')로 변환해줍니다.
    web_image_path = save_path.replace("\\", "/")
    # 프론트엔드가 접근할 완전한 이미지 웹 URL 주소 구성
    full_image_url = f"http://localhost:8000/{web_image_path}"

    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. YOLOv8 추론 실행
    results = yolo_model(save_path)
    
    # YOLO 결과물에서 클래스명과 확신도(confidence) 추출하기
    detected_class = "normal"  # 기본값 정상
    max_confidence = 0.0

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 모델이 정의한 클래스 인덱스를 가져와 이름으로 변환 (0: jump, 1: down, 2: normal 등)
            class_id = int(box.cls[0])
            class_name = yolo_model.names[class_id]  # 'jump', 'down', 'normal'
            confidence = float(box.conf[0])
            
            # 가장 확신도가 높은 객체 하나를 기준으로 잡음
            if confidence > max_confidence:
                max_confidence = confidence
                detected_class = class_name

    # 3. ★ 핵심 조건문 ★ jump 또는 down인 경우에만 DB 저장 및 웹소켓 알림 발생
    if detected_class in ["jump", "down"]:
        
        # [A] 조건 만족 시 DB 저장
        new_log = Detection_table(
            event_type=detected_class,   # "jump" 또는 "down"이 들어감
            confidence=round(max_confidence, 2), 
            gate_id=1,                   # 테스트용 게이트 아이디 (필요시 조정)
            image_path=save_path         # 증거 사진 경로 저장
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        # [B] 조건 만족 시 실시간 웹소켓 알림 전송
        await manager.broadcast({
            "event": "INTRUSION_DETECTED",
            "data": {
                "id": new_log.id,
                "gate": new_log.gate_id,
                "event_type": new_log.event_type,
                "confidence": new_log.confidence,
                "time": new_log.detected_at.strftime("%Y-%m-%d %H:%M:%S"),
                "image_url": full_image_url  # 프론트에서 띄울 이미지 주소
            }
        })
        
        return {
            "status": "intrusion_detected", 
            "event_type": detected_class, 
            "confidence": max_confidence,
            "image_url": full_image_url
        }

# 4. 'normal'인 경우 (무단침입이 아닌 정상 통행)
    else:
        # [A] 📡 웹소켓 알림 전송 코드를 완전히 제거하거나 주석 처리합니다.
        # (프론트엔드로 신호 자체를 보내지 않음)
        print("🍏 정상 통행이 감지되어 알림을 전송하지 않습니다.")

        # [B] 🧹 서버 용량을 위해 임시 저장했던 정상 통행 이미지를 디스크에서 완전히 삭제합니다.
        if os.path.exists(save_path):
            os.remove(save_path)
        print(f"🗑️ 정상 통행 이미지 삭제 완료: {save_path}")
            
        return {
            "status": "safe", 
            "message": "정상 통행이 감지되어 기록 및 이미지가 삭제되었습니다."
        }
        