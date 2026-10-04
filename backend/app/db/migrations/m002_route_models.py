"""เพิ่ม schema สำหรับ feature route: ScrapRequest, SellerProfile, PriceReference (T-02)"""
from app.db.session import Base
from app.db import models  # noqa: F401  ให้ SQLAlchemy รู้โมเดล route ก่อน create_all


def upgrade(engine) -> None:
    Base.metadata.create_all(engine)
