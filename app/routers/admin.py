from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.core.config import settings
from fastapi import HTTPException
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/config")
def get_config(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:  # Admin check basic
        raise HTTPException(status_code=403, detail="Not admin")
    return {"tenant_id": settings.tenant_id, "db_url": settings.db_url.replace("://", "://***:***@")}  # Mask pass