from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
import datetime

class Hotspot(Base):
    __tablename__ = "hotspots"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    frp = Column(Float)
    brightness = Column(Float)
    confidence = Column(String)
    satellite = Column(String)
    instrument = Column(String)
    acq_date = Column(String)
    acq_time = Column(String)
    fire_type = Column(String)
    confidence_score = Column(Float)
    is_chronic = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)