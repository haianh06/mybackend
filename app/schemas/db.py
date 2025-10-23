from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class CollectionCreate(BaseModel):
    name: str
    data: Optional[Dict[str, Any]] = {}

class CollectionUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None

class CollectionOut(BaseModel):
    id: int
    name: str
    data: Dict[str, Any]
    user_id: int
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True