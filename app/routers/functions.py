from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.services.tasks import send_email_task  # Placeholder

router = APIRouter(prefix="/functions", tags=["functions"])

@router.post("/{function_name}/run")
def run_function(function_name: str, payload: dict, current_user: User = Depends(get_current_user)):
    if function_name == "send_email":
        task = send_email_task.delay(payload.get("to"), payload.get("subject"), payload.get("body"))
        return {"task_id": task.id, "status": "queued"}
    else:
        raise HTTPException(status_code=404, detail="Function not found")