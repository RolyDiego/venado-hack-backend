from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Merchandiser(Base):
    __tablename__ = "merchandisers"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("supervisors.id"))