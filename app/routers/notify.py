from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.services.tasks import send_email_task  # Reuse

router = APIRouter(prefix="/notify", tags=["notifications"])

@router.post("/email")
def send_notification(to_email: str, subject: str, body: str, current_user: User = Depends(get_current_user)):
    task = send_email_task.delay(to_email, subject, body)
    return {"task_id": task.id, "status": "sent"}