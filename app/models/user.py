from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from app.core.database import Base
from app.core.config import settings

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tenant_id = Column(String, default=settings.tenant_id)