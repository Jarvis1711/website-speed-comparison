from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, db


def build_test_client(tmp_path):
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


def test_health_endpoint(tmp_path):
        client = build_test_client(tmp_path)
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json["status"] == "ok"


def test_create_item_api(tmp_path):
        client = build_test_client(tmp_path)
        response = client.post(
                "/api/items",
                json={"title": "Test item", "details": "A working record", "status": "active"},
        )
        assert response.status_code == 201
        assert response.json["title"] == "Test item"
