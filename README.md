# 🌐 Universal Backend - Self-Hosted BaaS (Backend as a Service)

**Universal Backend** là một **modular, self-hosted Backend as a Service (BaaS)** lấy cảm hứng từ Firebase.  
Nó được thiết kế để **tái sử dụng cho mọi dự án** (ví dụ như ứng dụng todo AIdoList của bạn).  
Dự án cung cấp các tính năng cốt lõi như:

> 🔐 Authentication, ⚡ Realtime CRUD Database, 📦 File Storage, ⚙️ Serverless Functions, 🔔 Notifications, 📊 Analytics, 🧩 Multi-tenant Admin Configs — tất cả trong **một hệ thống backend duy nhất.**

---

## 🚀 Tổng quan

Universal Backend được xây dựng bằng:
- **FastAPI** cho API
- **PostgreSQL** cho database
- **Redis** cho cache và realtime pub/sub
- **MinIO** cho lưu trữ file (S3-compatible)
- **Celery** cho xử lý background task

Hệ thống **được Docker hóa** giúp chạy nhanh trong local và **triển khai dễ dàng lên Render hoặc Heroku**.

---

## ✨ Features

| Tính năng | Mô tả |
|------------|--------|
| 🔑 **Auth** | JWT-based authentication với bcrypt hashing (`/auth/register`, `/auth/login`, `/auth/me`) |
| 💾 **Database** | CRUD động cho mọi collection (`/db/{collection}`), realtime broadcast qua Socket.IO, JSONB storage |
| 🗂 **Storage** | Upload/download/delete file qua MinIO với presigned URL |
| ⚙️ **Functions** | Serverless task chạy qua Celery (ví dụ: `send_email`) |
| 🔔 **Notifications** | Gửi email/push notification qua Celery (extendable sang FCM) |
| 📊 **Analytics/Monitoring** | Prometheus metrics endpoint (`/metrics`) cho health & performance |
| 🧭 **Admin/Configs** | Multi-tenant qua `tenant_id`; admin API cho config & migration |
| 🔒 **Security** | Rate limiting (SlowAPI), CORS, logging (structlog) |
| 🔁 **Realtime** | WebSocket (Socket.IO) phát sự kiện khi dữ liệu thay đổi |
| 🧩 **Modular** | Dễ mở rộng và thêm router/service mới |

---

## 🧱 Tech Stack

| Thành phần | Công nghệ |
|-------------|------------|
| **Backend** | FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL (JSONB universal DB) |
| **Cache/Realtime** | Redis (Pub/Sub cho Celery và Socket.IO) |
| **Storage** | MinIO (S3-compatible, có thể thay AWS S3) |
| **Tasks** | Celery (broker/result backend: Redis) |
| **Security** | JWT (python-jose), bcrypt (passlib), SlowAPI (rate limiting) |
| **Logging** | structlog |
| **Testing** | pytest |
| **Deployment** | Docker Compose (local), Render/Heroku (cloud) |

---

## 📂 Cấu trúc thư mục

```bash
universal-backend/
├── app/
│   ├── main.py                  # Entry point: FastAPI app, routers, middleware
│   ├── core/
│   │   ├── config.py            # Pydantic settings từ .env
│   │   ├── security.py          # JWT, password hash/verify
│   │   ├── database.py          # SQLAlchemy engine/session
│   │   └── redis.py             # Redis client
│   ├── models/
│   │   ├── user.py              # User model
│   │   └── collection.py        # Generic collection model (JSONB)
│   ├── routers/
│   │   ├── auth.py              # /auth endpoints
│   │   ├── db.py                # /db/{collection} CRUD
│   │   ├── storage.py           # File upload/download/delete
│   │   ├── functions.py         # /functions/{name}/run (Celery)
│   │   ├── notify.py            # /notify/email
│   │   └── admin.py             # /admin/config
│   ├── services/
│   │   ├── realtime.py          # Socket.IO
│   │   └── tasks.py             # Celery tasks
│   └── schemas/
│       ├── auth.py              # UserCreate, Token schemas
│       └── db.py                # CollectionCreate/Update/Out
├── migrations/                  # Alembic migrations
├── tests/                       # pytest tests
├── docker-compose.yml           # Services: db, redis, minio, backend, celery
├── Dockerfile                   # Python 3.12-slim
├── requirements.txt             # Dependencies
├── .env                         # Environment variables
└── README.md
