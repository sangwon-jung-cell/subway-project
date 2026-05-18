from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import os

from database import Base, engine
from api import detection
# manager.py에서 생성된 싱글톤 manager 객체와 ConnectionManager 클래스를 명확히 가져옴
from manager import manager, ConnectionManager

app = FastAPI()

# 1. 데이터베이스 테이블 자동 생성 (없을 때만 생성됨)
Base.metadata.create_all(bind=engine)

# 2. 정적 파일(이미지 저장용) 폴더 생성 및 마운트
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. 메인 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Subway Detection API Platform"}

# 4. 웹소켓 엔드포인트 라우팅 (프론트엔드 실시간 연결용)
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    # manager.py에서 가져온 공용 manager 객체를 사용합니다.
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # 연결 유지를 위한 대기 및 핑퐁
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 5. 분리한 탐지 API 라우터 등록 (중복 제거 후 하단에 한 번만 배치)
app.include_router(detection.router, prefix="/detect", tags=["Detection"])