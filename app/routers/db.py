from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.collection import Collection
from app.schemas.db import CollectionCreate, CollectionUpdate, CollectionOut
from app.services.realtime import broadcast_update
from app.core.config import settings
from sqlalchemy import func
router = APIRouter(prefix="/db", tags=["database"])

@router.post("/{collection_name}", response_model=CollectionOut)
def create_collection(collection_name: str, item: CollectionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if collection_name != item.name:
        raise HTTPException(status_code=400, detail="Collection name mismatch")
    db_item = Collection(name=item.name, data=item.data, user_id=current_user.id, tenant_id=settings.tenant_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    broadcast_update(collection_name, "create", db_item.id, db_item.data)  # Realtime
    return db_item

@router.get("/{collection_name}", response_model=List[CollectionOut])
def read_collections(collection_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(Collection).filter(Collection.name == collection_name, Collection.user_id == current_user.id, Collection.tenant_id == settings.tenant_id).all()
    return items

@router.put("/{collection_name}/{item_id}", response_model=CollectionOut)
def update_collection(collection_name: str, item_id: int, item: CollectionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Collection).filter(Collection.id == item_id, Collection.name == collection_name, Collection.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.data is not None:
        db_item.data = item.data
        db_item.updated_at = func.now()
    db.commit()
    db.refresh(db_item)
    broadcast_update(collection_name, "update", db_item.id, db_item.data)
    return db_item

@router.delete("/{collection_name}/{item_id}")
def delete_collection(collection_name: str, item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Collection).filter(Collection.id == item_id, Collection.name == collection_name, Collection.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    broadcast_update(collection_name, "delete", db_item.id, None)
    return {"detail": "Deleted"}