# Website Speed Comparison

## Overview
Compares two URLs side-by-side using Lighthouse API data.

## Tech Stack
- Python 3
- Flask
- SQLite + SQLAlchemy ORM
- Gunicorn + Docker
- Pytest + GitHub Actions CI

## Features
- Beautiful dashboard UI with status cards and responsive layout
- Full CRUD for core work items
- JSON API endpoints for integration (`/api/health`, `/api/items`)
- Ready-to-deploy setup (Dockerfile, docker-compose, Procfile)
- CI workflow for basic smoke checks

## Local Run
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000/`.

## Docker Run
```bash
docker compose up --build
```

## Deploy
- `Procfile` supports PaaS deployment (Render/Railway/Heroku-style)
- `Dockerfile` supports container deployments (ECS, Fly.io, DigitalOcean, etc.)

## Proof of Concept
See [proof-of-concept.md](proof-of-concept.md), [proof/demo-output.txt](proof/demo-output.txt), and [proof/ui-preview.svg](proof/ui-preview.svg).
