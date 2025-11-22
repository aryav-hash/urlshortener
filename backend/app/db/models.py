from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

# Indexing being used here
class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, unique=True)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiry = Column(DateTime, nullable=True)
