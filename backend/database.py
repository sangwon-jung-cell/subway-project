from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import os
from sqlalchemy.ext.declarative import declarative_base

# 1. Base 선언 (중복되었던 부분 하나로 통합)
Base = declarative_base()

# 도커 컴포즈에서 설정한 환경 변수를 가져옵니다.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/subway_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# db 연결 세션 관리 (팀원이 추가한 핵심 로직)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 아래는 상원님이 정의하신 테이블 모델들 ---

# 1. 관리자 테이블
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# 2. 행위 로그 테이블 (핵심 데이터 저장)
class Detection_table(Base):
    __tablename__ = "detection_logs"
    id = Column(Integer, primary_key=True, index=True)
    gate_id = Column(Integer)
    
    # 감지 정보
    event_type = Column(String)  # jump or down
    confidence = Column(Float)   # YOLO 모델의 확신도
    
    # 증거 데이터
    image_path = Column(String)  # 서버 내 static 폴더에 저장된 이미지 경로
    
    # 시간 정보
    detected_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class Gates(Base):
    __tablename__ = "Gates"
    id = Column(Integer, primary_key=True, index=True)
    gate_name = Column(String)

class Station(Base):
    __tablename__ = "Station"
    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String, unique=True)