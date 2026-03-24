# Website Speed Comparison

## Solution Summary
Production-ready domain application.

This Phase-2 implementation is a domain-ready, deployable web application for **Developer Experience** workflows.

## Core Capabilities
- Responsive dashboard with KPI cards and recent activity table
- Domain record lifecycle with full CRUD (web + API)
- Dynamic schema fields tailored to this use case
- Status pipeline: `captured, implementing, review, released`
- Docker + Gunicorn deployment assets, CI checks, and Pytest tests

## Domain Model
- Primary entity: **Website Speed Engineering Item**
- Collection: **Website Speed Engineering Items**
- Dynamic fields:
- Repository (`repository` / text)
- Impact Score (`impact_score` / number)
- Technical Notes (`technical_notes` / textarea)

## Operational Workflow
1. Capture requirement
2. Build implementation
3. Review quality
4. Release value

## API
- `GET /api/health`
- `GET /api/schema`
- `GET /api/records`
- `POST /api/records`
- `GET /api/metrics`

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Docker Run
```bash
docker compose up --build
```

## Proof of Concept
- [proof-of-concept.md](proof-of-concept.md)
- [proof/demo-output.txt](proof/demo-output.txt)
- [proof/ui-preview.svg](proof/ui-preview.svg)
