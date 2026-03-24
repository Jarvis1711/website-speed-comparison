# Proof of Concept - Website Speed Comparison

## Scope
- App category: Developer Experience
- Entity model: Website Speed Engineering Item
- Deployable stack: Flask + SQLAlchemy + Gunicorn + Docker + CI

## Dynamic Field Configuration
- Repository: `repository` (text)
- Impact Score: `impact_score` (number)
- Technical Notes: `technical_notes` (textarea)

## Run Evidence Commands
```bash
python app.py
curl http://localhost:5000/api/health
curl http://localhost:5000/api/schema
curl -X POST http://localhost:5000/api/records   -H "Content-Type: application/json"   -d '{"title":"Demo Record","status":"implementing","payload":{"repository":"Demo value","impact_score":12,"technical_notes":"seed note"}}'
curl http://localhost:5000/api/metrics
```

## Metadata
- Idea number: 99
- Generated UTC: 2026-03-24T15:52:22.546744+00:00
- Status: Phase-2 complete
