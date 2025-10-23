from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Collection name, e.g., "todos"
    data = Column(JSON)  # Generic data: {"title": "Buy milk", "done": false}
    user_id = Column(Integer, ForeignKey("users.id"))
    tenant_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())