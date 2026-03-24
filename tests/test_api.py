from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, db
from app.schemas import FIELD_SCHEMA


def build_client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        }
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client()


def payload():
    out = {}
    for field in FIELD_SCHEMA:
        out[field["key"]] = 10 if field["type"] == "number" else "demo"
    return out


def test_health(tmp_path):
    client = build_client(tmp_path)
    response = client.get("/api/health")
    assert response.status_code == 200


def test_create_item(tmp_path):
    client = build_client(tmp_path)
    response = client.post("/api/items", json={"title": "x", "payload": payload()})
    assert response.status_code == 201
