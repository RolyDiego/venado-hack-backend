from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class MarketCategory(Base):
    __tablename__ = "market_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    icon_name = Column(String(50), nullable=False)

    tasks = relationship("CategoryTask", back_populates="category", cascade="all, delete-orphan")
    markets = relationship("Market", back_populates="category")


class CategoryTask(Base):
    __tablename__ = "category_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("market_categories.id", ondelete="CASCADE"), nullable=False)
    task_description = Column(String(255), nullable=False)
    estimated_time_mins = Column(Integer, nullable=False)

    category = relationship("MarketCategory", back_populates="tasks")


class OptimizedRoute(Base):
    __tablename__ = "optimized_routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin_lat = Column(Numeric(12, 8), nullable=False)
    origin_lng = Column(Numeric(12, 8), nullable=False)
    destination_ids_hash = Column(String(64), nullable=False, unique=True)
    optimized_path_json = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False)
