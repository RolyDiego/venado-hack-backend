from sqlalchemy import Column, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class CustomerVisitDay(Base):
    __tablename__ = "customer_visit_days"

    id = Column(UUID(as_uuid=True), primary_key=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    day_of_week = Column(SmallInteger, nullable=False)