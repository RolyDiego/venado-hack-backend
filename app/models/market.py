from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Market(Base):
    __tablename__ = "markets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)