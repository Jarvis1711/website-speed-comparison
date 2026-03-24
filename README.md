# Website Speed Comparison

## Phase 3 Upgrade Summary
Production-oriented developer experience solution for website speed comparison workflows.

## Domain Context
- Domain: **Developer Experience**
- Core Entity: **Engineering Initiative**
- Lifecycle Statuses: `planned, building, testing, released`

## Architecture
- Flask application factory pattern (`app/__init__.py`)
- Layered backend (`routes` → `services` → `repositories`)
- SQLAlchemy persistence with JSON payload modeling
- REST API + HTML dashboard + CSV exports
- Deployment surfaces (`Dockerfile`, `docker-compose.yml`, `Procfile`, `wsgi.py`)

## Capability Set
- Role-ready modular architecture (routes, services, repositories)
- Operational dashboard with status metrics and pipeline view
- CRUD workflows via web UI and REST API
- CSV export endpoint for reporting
- Ready for production via Gunicorn, Docker, and Procfile
- Developer-centric API surfaces and metrics endpoint

## Dynamic Schema
- Repository (`repo` / text)
- Risk Score (`risk_score` / number)
- Technical Notes (`technical_notes` / textarea)

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## API Highlights
- `GET /api/health`
- `GET /api/schema`
- `GET /api/items`
- `POST /api/items`
- `PUT /api/items/<id>`
- `DELETE /api/items/<id>`
- `GET /api/metrics`

## Proof of Concept
- [proof-of-concept.md](proof-of-concept.md)
- [proof/demo-output.txt](proof/demo-output.txt)
- [proof/ui-preview.svg](proof/ui-preview.svg)
- [proof/architecture.md](proof/architecture.md)
