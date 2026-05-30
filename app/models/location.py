from sqlalchemy import Column, Numeric, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base

class MerchandiserLocation(Base):
    __tablename__ = "merchandiser_locations"

    merchandiser_id = Column(UUID(as_uuid=True), ForeignKey("merchandisers.id"), primary_key=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    accuracy = Column(Numeric(10, 2), nullable=True)
    speed = Column(Numeric(10, 2), nullable=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class MerchandiserLocationHistory(Base):
    __tablename__ = "merchandiser_location_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    merchandiser_id = Column(UUID(as_uuid=True), ForeignKey("merchandisers.id"), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    accuracy = Column(Numeric(10, 2), nullable=True)
    speed = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
