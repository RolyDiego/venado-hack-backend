from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(String(50), nullable=False)
    customer_name = Column(String(200), nullable=False)
    category = Column(String(50))
    market_id = Column(UUID(as_uuid=True), ForeignKey("markets.id"), nullable=False)
    latitude = Column(Numeric(12, 8))
    longitude = Column(Numeric(12, 8))
    visit_duration_minutes = Column(Integer, nullable=False)
    merchandiser_id = Column(UUID(as_uuid=True), ForeignKey("merchandisers.id"))
    created_at = Column(DateTime)