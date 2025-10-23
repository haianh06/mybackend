from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    secret_key: str
    db_url: str
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    tenant_id: str = "default_tenant"

    class Config:
        env_file = ".env"

settings = Settings()