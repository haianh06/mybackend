from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
import structlog
from prometheus_client import make_asgi_app
import socketio
from starlette.requests import Request
from fastapi import HTTPException
from app.core.database import engine, get_db, Base, SessionLocal
from app.core.redis import redis_client
from app.routers import auth, db, storage, functions, notify, admin
from app.services.realtime import app as sio_app
from app.core.config import settings


# Logging
logger = structlog.get_logger()

# FastAPI app
app = FastAPI(title="Universal Backend", version="1.0.0")

# Rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware logging & metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request", method=request.method, path=request.url.path)
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth.router)
app.include_router(db.router)
app.include_router(storage.router)
app.include_router(functions.router)
app.include_router(notify.router)
app.include_router(admin.router)

# Mount Socket.IO
app.mount("/socket.io", sio_app)

# Prometheus metrics
app.mount("/metrics", make_asgi_app())

# Health check
@app.get("/health")
async def health():
    try:
        await redis_client.ping()
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db.commit()
        finally:
            db.close()
        return {"status": "healthy", "db": "connected", "redis": "pinged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Create tables
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    await redis_client.ping()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)