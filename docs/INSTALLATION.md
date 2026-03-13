# Installation & Deployment Guide

## Option 1: Self-hosted with Docker (recommended for institutions)

Requires: Docker Desktop or Docker Engine + Compose

```bash
git clone https://github.com/your-username/pdf-highlight-extractor.git
cd pdf-highlight-extractor
docker compose -f docker/docker-compose.yml up
```

Open http://localhost:80. All PDFs stay on your machine.

**To run in the background:**
```bash
docker compose -f docker/docker-compose.yml up -d
```

**To stop:**
```bash
docker compose -f docker/docker-compose.yml down
```

---

## Option 2: Deploy to the cloud (Vercel + Railway)

### Backend → Railway

1. Create a free account at railway.app
2. New Project → Deploy from GitHub repo → select `pdf-highlight-extractor`
3. Set root directory to `backend`
4. Add environment variable: `ALLOWED_ORIGINS=["https://your-vercel-app.vercel.app"]`
5. Copy the Railway deployment URL (e.g. `https://pdf-highlight-extractor.up.railway.app`)

### Frontend → Vercel

1. Create a free account at vercel.com
2. Import GitHub repo → set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-railway-url.up.railway.app`
4. Deploy

---

## Option 3: Local development (no Docker)

See the [README](../README.md#quick-start) for step-by-step instructions.
