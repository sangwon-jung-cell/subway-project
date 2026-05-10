from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# static 폴더가 없으면 자동으로 생성해주는 로직 (선택사항)
if not os.path.exists("static"):
    os.makedirs("static")

# 'static' 경로로 들어오는 요청을 현재 실행 위치의 'static' 폴더와 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Subway Detection API"}