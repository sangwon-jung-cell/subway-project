from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import os


# 도커 컴포즈에서 설정한 환경 변수를 가져옵니다. 없을 경우 기본값 사용.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/subway_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# 1. 관리자 테이블 (로그인 및 설정용)
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# 2. 행위 로그 테이블 (핵심 데이터 저장)
class IntrusionLog(Base):
    __tablename__ = "intrusion_logs"
    id = Column(Integer, primary_key=True, index=True)
    
    # 감지 정보
    event_type = Column(String)  # 'Jumping' 또는 'Crawling'
    confidence = Column(Float)   # YOLO 모델의 확신도 (예: 0.85)
    
    # 증거 데이터
    image_path = Column(String)  # 서버 내 static 폴더에 저장된 이미지 경로
    
    # 시간 정보
    # utcnow 대신 local 시간을 쓰고 싶다면 서비스 성격에 맞춰 조정 가능합니다.
    detected_at = Column(DateTime, default=datetime.datetime.utcnow, index = True)

