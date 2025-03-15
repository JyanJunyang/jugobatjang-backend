from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.model.base_model import BaseModel


class Excels(BaseModel, table=True):
    """엑셀 테이블"""

    __tablename__ = "excels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(225), nullable=False)
    upload_date = Column(DateTime, default=func.now())
    share_count = Column(Integer, default=0)
    max_share_count = Column(Integer, default=10)
