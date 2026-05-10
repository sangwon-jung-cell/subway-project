from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import os


# 도커 컴포즈에서 설정한 환경 변수를 가져옵니다. 없을 경우 기본값 사용.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/subway_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. 관리자 테이블
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

# 2. 개찰구 테이블


# 3. 행위 로그 테이블
class IntrusionLog(Base):
    __tablename__ = "intrusion_logs"
    id = Column(Integer, primary_key=True)
    gate_id = Column(String, ForeignKey("gates.id"))
    event_type = Column(String) # Jumping, Crawling
    bbox_coords = Column(JSON)  # [x, y, w, h]
    confidence = Column(Float)  # 신뢰도
    image_path = Column(String) # 이미지 경로
    detected_at = Column(DateTime, default=datetime.datetime.utcnow) # 감지된 시간
