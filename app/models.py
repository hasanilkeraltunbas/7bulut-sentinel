from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from .database import Base
from datetime import datetime, timedelta, timezone

# Türkiye saatini (UTC+3) tanımlayalım
TR_TIME = timezone(timedelta(hours=3))

class MonitorLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    # default kısmını Türkiye saatine göre güncelledik
    timestamp = Column(DateTime, default=lambda: datetime.now(TR_TIME), index=True)
    is_online = Column(Boolean)
    response_time = Column(Float)
    zeytin_status = Column(Boolean)
    status_code = Column(Integer)