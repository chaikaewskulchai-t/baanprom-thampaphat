"""สร้าง engine และ session ของ SQLAlchemy (ทีมเลือกเอง ไม่ได้มาจาก spec)"""
import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool

from app import config


class Base(DeclarativeBase):
    pass


def make_engine(url: str = config.DATABASE_URL):
    # SQLite ในหน่วยความจำทำงานไม่เสถียรเมื่อหลาย thread เข้าถึงพร้อมกัน
    # จึงใช้ไฟล์ชั่วคราวแทน URL ใน-memory เพื่อให้ session/connection ใช้งานร่วมกันได้ปลอดภัย
    if url.startswith("sqlite"):
        if url.startswith("sqlite:///:memory:"):
            fd, db_path = tempfile.mkstemp(prefix="baanprom_", suffix=".db")
            os.close(fd)
            url = f"sqlite:///{db_path}"
        return create_engine(
            url, connect_args={"check_same_thread": False}, poolclass=NullPool
        )
    return create_engine(url)


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
