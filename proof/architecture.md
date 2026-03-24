# Architecture Notes

## Layers
1. `app/routes` handles HTTP concerns (web + API)
2. `app/services` enforces business rules and metrics logic
3. `app/repositories` performs persistence operations
4. `app/models` stores state in SQLite (production-ready swap to Postgres via URI)

## Domain Fit
- Domain: Developer Experience
- Entity: Engineering Initiative
- Field strategy: dynamic schema encoded in `app/schemas.py`

## Deployment
- Container: `Dockerfile`
- Compose: `docker-compose.yml`
- PaaS process: `Procfile`
- WSGI entrypoint: `wsgi.py`
