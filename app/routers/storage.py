from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
import uuid

router = APIRouter(prefix="/storage", tags=["storage"])
minio_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False  # Local, true for S3
)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not file.content_type.startswith('image/') and not file.content_type.startswith('application/'):  # Basic check
        raise HTTPException(status_code=400, detail="File type not allowed")
    file_id = str(uuid.uuid4())
    bucket_name = f"user_{current_user.id}_bucket"
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        minio_client.put_object(bucket_name, file_id, file.file, length=-1, part_size=10*1024*1024)
        presigned_url = minio_client.presigned_get_object(bucket_name, file_id)
        return {"file_id": file_id, "url": presigned_url}
    except S3Error as err:
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Assume file_id includes user prefix or check ownership
    bucket_name = f"user_{current_user.id}_bucket"
    try:
        presigned_url = minio_client.presigned_get_object(bucket_name, file_id)
        return {"url": presigned_url}
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")

@router.delete("/{file_id}")
def delete_file(file_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bucket_name = f"user_{current_user.id}_bucket"
    try:
        minio_client.remove_object(bucket_name, file_id)
        return {"detail": "Deleted"}
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")