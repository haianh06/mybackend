Universal Backend - Self-Hosted BaaS (Backend as a Service)

Universal Backend is a modular, self-hosted Backend as a Service (BaaS) inspired by Firebase. It's designed to be reusable for any project (e.g., your AIdoList todo app). It provides core features like authentication, realtime CRUD database, file storage, serverless functions, notifications, analytics, and multi-tenant admin configs—all in one universal setup.
This project uses FastAPI for the API, PostgreSQL for the database, Redis for caching/realtime, MinIO for storage, and Celery for tasks. It's Dockerized for easy local dev and deployable to Render/Heroku.
Features

Auth: JWT-based authentication with bcrypt hashing (register, login, me endpoints).
Database: Generic CRUD operations on collections (e.g., /db/todos) with realtime broadcasts via Socket.IO and JSONB storage in PostgreSQL.
Storage: File upload/download/delete with MinIO (S3-compatible) and presigned URLs.
Functions: Serverless tasks via Celery (e.g., run custom functions like send_email).
Notifications: Basic push/email sending (integrated with Celery tasks; extendable to FCM).
Analytics/Monitoring: Prometheus metrics endpoint (/metrics) for health and performance.
Admin/Configs: Multi-tenant support via tenant_id; admin endpoints for configs and migrations.
Security: Rate limiting (SlowAPI), CORS, middleware logging (structlog).
Realtime: WebSocket broadcasts for DB changes (Socket.IO).
Modular: Easy to extend for new routers/services.

Tech Stack

Backend: FastAPI (API), SQLAlchemy (ORM), Alembic (migrations).
Database: PostgreSQL (universal_db with JSONB for generic data).
Cache/Realtime: Redis (pub/sub for Celery and Socket.IO).
Storage: MinIO (local S3-compatible; swap to AWS S3).
Tasks: Celery (broker/result backend: Redis).
Security: JWT (python-jose), bcrypt (passlib), rate limiting (slowapi).
Logging: structlog.
Testing: pytest.
Deployment: Docker Compose (local), Render/Heroku (cloud).

Project Structure
textuniversal-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point: FastAPI app, routers, middleware
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic settings from .env
│   │   ├── security.py          # JWT, password hash/verify
│   │   ├── database.py          # SQLAlchemy engine/session
│   │   └── redis.py             # Async Redis client
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model (id, username, email, hashed_password, tenant_id)
│   │   └── collection.py        # Generic Collection (name, data JSONB, user_id, tenant_id)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py              # /auth/register, /login, /me
│   │   ├── db.py                # /db/{collection} CRUD + realtime
│   │   ├── storage.py           # /storage/upload, get, delete
│   │   ├── functions.py         # /functions/{name}/run (Celery)
│   │   ├── notify.py            # /notify/email (Celery task)
│   │   └── admin.py             # /admin/config (multi-tenant)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── realtime.py          # Socket.IO events/broadcast
│   │   └── tasks.py             # Celery app/tasks (e.g., send_email)
│   └── schemas/
│       ├── __init__.py
│       ├── auth.py              # UserCreate, Token schemas
│       └── db.py                # CollectionCreate/Update/Out
├── migrations/                  # Alembic migrations
├── tests/                       # pytest tests
├── docker-compose.yml           # Services: db, redis, minio, backend, celery
├── Dockerfile                   # Python 3.12-slim build
├── requirements.txt             # Dependencies (fastapi, sqlalchemy, etc.)
├── .env                         # Secrets (DB_URL, SECRET_KEY, etc.)
└── README.md                    # This file
Prerequisites

Python 3.12 (from python.org; add to PATH).
Docker Desktop (with WSL2 enabled for Windows).
Git (for repo management).
GitHub Account (for deployment).
Optional: VS Code for editing.

On Windows: Use CMD or PowerShell; run as Admin if permission issues.
Installation & Local Setup


Clone Repo:
textgit clone https://github.com/yourusername/universal-backend.git
cd universal-backend


Install Dependencies (local dev):
textpip install -r requirements.txt


Setup .env:

Copy .env.example to .env.
Fill values:
textSECRET_KEY=your_super_secret_key_here  # Gen: python -c "import secrets; print(secrets.token_urlsafe(32))"
DB_URL=postgresql://postgres:password@db:5432/universal_db
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
TENANT_ID=default_tenant

Note: For production, use strong secrets and external services (e.g., AWS RDS for DB).



Init Alembic Migrations:
textalembic init migrations

Edit migrations/env.py: Add imports for models and target_metadata = Base.metadata.
Edit alembic.ini: sqlalchemy.url = %(DB_URL)s.
Gen initial migration: alembic revision --autogenerate -m "Initial".



Run Local (Docker Compose):
textdocker-compose up --build

Services: Postgres (db:5432), Redis (6379), MinIO (9000/9001), Backend (8000), Celery worker.
Access: http://localhost:8000/docs (Swagger UI).
Run migration: docker-compose exec backend alembic upgrade head.
Stop: Ctrl+C, then docker-compose down -v (clean volumes).

Troubleshooting:

DB connect fail: Check .env DB_URL; reset volumes docker-compose down -v.
Port conflict: Change ports in docker-compose.yml.



API Testing
Use Swagger: http://localhost:8000/docs (Authorize with Bearer token from /auth/login).

Auth:

POST /auth/register: {"username": "test", "email": "test@example.com", "password": "secret"}.
POST /auth/login: Same → Get token.
GET /auth/me: With token.


Database (CRUD):

POST /db/todos: {"name": "todos", "data": {"title": "Buy milk", "done": false}} → Create.
GET /db/todos: List items.
PUT /db/todos/1: {"data": {"done": true}} → Update.
DELETE /db/todos/1: Delete.
Realtime: Use Socket.IO client to listen 'update' events.


Storage:

POST /storage/upload: Upload file → Presigned URL.
GET /storage/{file_id}: Download URL.
DELETE /storage/{file_id}.


Functions/Notify:

POST /functions/send_email/run: {"to": "email", "subject": "Hi", "body": "Test"}.
POST /notify/email: Query params (to_email, subject, body).


Health/Metrics:

GET /health: {"status": "healthy"}.
GET /metrics: Prometheus data.



Realtime Test: Create test_realtime.html with Socket.IO script; connect to ws://localhost:8000/socket.io.
Unit Tests: pytest tests/ (add fixtures for DB).
Deployment
Render (Recommended - Free Tier)

Push to GitHub: git add .; git commit -m "Initial"; git push.
On Render.com:

New > Web Service > Connect GitHub repo.
Docker runtime; Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT.
Env Vars: From .env (update DB_URL to Render Postgres add-on URL; Redis: Upstash free; MinIO: AWS S3 keys).
New > Background Worker for Celery: Same env, Start: celery -A app.services.tasks worker --loglevel=info.


Build Script (for migration): docker run --rm -e DB_URL=$DB_URL app alembic upgrade head.
Live: https://yourapp.onrender.com/docs.

Notes: Free tier sleeps after 15min; ping /health to wake. For prod: Paid plans, external DB/S3.
Heroku Alternative

Use Heroku CLI: heroku create; git push heroku main.
Add-ons: Heroku Postgres, Redis; set config vars from .env.
Procfile: web: uvicorn app.main:app --host=0.0.0.0 --port=$PORT; worker: celery -A app.services.tasks worker.

Contributing

Fork repo.
Create branch: git checkout -b feature/new-module.
Commit: git commit -m "Add new feature".
Push: git push origin feature/new-module.
Open PR.

Guidelines: Follow PEP8; add tests; update README.
License
MIT License - see LICENSE file (create if missing).
Support

Issues: GitHub Issues.
Questions: Open discussion or contact maintainer.


Built with ❤️ by [Your Name] for reusable BaaS projects like AIdoList. Contributions welcome!


Quick Start Script (for new users):
bashgit clone <repo> && cd universal-backend
cp .env.example .env  # Edit secrets
docker-compose up --build
# Migrate: docker-compose exec backend alembic upgrade head
# Test: http://localhost:8000/docs
