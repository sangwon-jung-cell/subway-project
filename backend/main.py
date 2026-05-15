from api import detection
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from database import Base, engine  # models.py에서 정의한 Base와 engine 임포트

app = FastAPI()

# main.py 또는 데이터베이스 초기화 부분
# 이 코드가 실행되는 시점에 테이블이 생성됩니다.
Base.metadata.create_all(bind=engine)


# static 폴더가 없으면 자동으로 생성해주는 로직 (선택사항)
if not os.path.exists("static"):
    os.makedirs("static")

# 'static' 경로로 들어오는 요청을 현재 실행 위치의 'static' 폴더와 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# 분리한 라우터를 등록 (prefix를 주면 주소가 /detect/test-model 식으로 바뀜)
app.include_router(detection.router, prefix="/detect", tags=["Detection"])

@app.get("/")
def read_root():
    return {"message": "Subway Detection API"}