from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    market_id = Column(UUID(as_uuid=True), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    visit_duration_minutes = Column(Integer, nullable=False)
    merchandiser_id = Column(UUID(as_uuid=True), ForeignKey("merchandisers.id"), nullable=False)

    visit_days = relationship("CustomerVisitDay", back_populates="customer", cascade="all, delete-orphan")


class CustomerVisitDay(Base):
    __tablename__ = "customer_visit_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    day_of_week = Column(SmallInteger, nullable=False)  # 1=Monday, 2=Tuesday, etc.

    customer = relationship("Customer", back_populates="visit_days")


class Merchandiser(Base):
    __tablename__ = "merchandisers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), nullable=True)

    customers = relationship("Customer", backref="merchandiser")
