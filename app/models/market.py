from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Market(Base):
    __tablename__ = "markets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("market_categories.id"), nullable=True)

    category = relationship("MarketCategory", back_populates="markets")
    customers = relationship("Customer", back_populates="market")