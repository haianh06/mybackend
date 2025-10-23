# 🌐 Universal Backend - Self-Hosted BaaS (Backend as a Service)

**Universal Backend** is a **modular, self-hosted Backend as a Service (BaaS)** inspired by Firebase.  
It’s designed to be **reusable across all your projects** (for example, the AIdoList Todo App).  
The system provides all essential backend features such as:

> 🔐 Authentication, ⚡ Realtime CRUD Database, 📦 File Storage, ⚙️ Serverless Functions, 🔔 Notifications, 📊 Analytics, 🧩 Multi-tenant Admin Configs — all in **one unified backend platform.**

---

## 🚀 Overview

Universal Backend is built with:
- **FastAPI** for the REST API
- **PostgreSQL** for database storage
- **Redis** for caching and realtime pub/sub
- **MinIO** for file storage (S3-compatible)
- **Celery** for background task processing

The system is **fully containerized with Docker**, allowing easy local development and **seamless deployment to Render or Heroku**.

---

## ✨ Features

| Feature | Description |
|----------|--------------|
| 🔑 **Auth** | JWT-based authentication with bcrypt hashing (`/auth/register`, `/auth/login`, `/auth/me`) |
| 💾 **Database** | Dynamic CRUD for any collection (`/db/{collection}`), realtime broadcasting via Socket.IO, JSONB data storage |
| 🗂 **Storage** | Upload, download, and delete files via MinIO using presigned URLs |
| ⚙️ **Functions** | Serverless task execution through Celery (e.g., `send_email`) |
| 🔔 **Notifications** | Send email or push notifications via Celery (extendable to FCM) |
| 📊 **Analytics / Monitoring** | Prometheus metrics endpoint (`/metrics`) for health and performance tracking |
| 🧭 **Admin / Configs** | Multi-tenant management with `tenant_id`; admin APIs for config and migration |
| 🔒 **Security** | Rate limiting (SlowAPI), CORS, and structured logging (structlog) |
| 🔁 **Realtime** | WebSocket (Socket.IO) events when data changes |
| 🧩 **Modular Architecture** | Easily extendable with new routers or services |

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL (JSONB universal database) |
| **Cache / Realtime** | Redis (Pub/Sub for Celery and Socket.IO) |
| **Storage** | MinIO (S3-compatible; can be replaced with AWS S3) |
| **Task Queue** | Celery (Redis as broker and result backend) |
| **Security** | JWT (python-jose), bcrypt (passlib), SlowAPI (rate limiting) |
| **Logging** | structlog |
| **Testing** | pytest |
| **Deployment** | Docker Compose (local), Render / Heroku (cloud) |

---
