from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import FIELD_SCHEMA, create_app, db


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


def sample_payload():
    payload = {}
    for field in FIELD_SCHEMA:
        if field["input_type"] == "number":
            payload[field["key"]] = 42
        else:
            payload[field["key"]] = "demo"
    return payload


def test_health(tmp_path):
    client = build_client(tmp_path)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_create_record(tmp_path):
    client = build_client(tmp_path)
    response = client.post(
        "/api/records",
        json={"title": "Phase2", "payload": sample_payload()},
    )
    assert response.status_code == 201
    listing = client.get("/api/records")
    assert listing.status_code == 200
    assert len(listing.json) == 1
