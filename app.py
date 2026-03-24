from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class WorkItem(db.Model):
    __tablename__ = "work_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="planned", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        APP_TITLE="Website Speed Comparison",
        APP_DESCRIPTION="Compares two URLs side-by-side using Lighthouse API data.",
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.get("/")
    def dashboard():
        items = WorkItem.query.order_by(WorkItem.created_at.desc()).all()
        counts = {
            "planned": WorkItem.query.filter_by(status="planned").count(),
            "active": WorkItem.query.filter_by(status="active").count(),
            "done": WorkItem.query.filter_by(status="done").count(),
        }
        return render_template("index.html", items=items, counts=counts)

    @app.route("/items/new", methods=["GET", "POST"])
    def create_item():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            details = request.form.get("details", "").strip()
            status = request.form.get("status", "planned").strip() or "planned"

            if not title or not details:
                return render_template("form.html", item=None, error="Title and details are required.")

            item = WorkItem(title=title, details=details, status=status)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("dashboard"))

        return render_template("form.html", item=None, error=None)

    @app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
    def edit_item(item_id):
        item = WorkItem.query.get_or_404(item_id)
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            details = request.form.get("details", "").strip()
            status = request.form.get("status", "planned").strip() or "planned"

            if not title or not details:
                return render_template("form.html", item=item, error="Title and details are required.")

            item.title = title
            item.details = details
            item.status = status
            db.session.commit()
            return redirect(url_for("dashboard"))

        return render_template("form.html", item=item, error=None)

    @app.post("/items/<int:item_id>/delete")
    def delete_item(item_id):
        item = WorkItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.get("/api/health")
    def health_check():
        return jsonify(status="ok", app=app.config["APP_TITLE"])

    @app.get("/api/items")
    def list_items():
        items = WorkItem.query.order_by(WorkItem.created_at.desc()).all()
        return jsonify([item.to_dict() for item in items])

    @app.post("/api/items")
    def create_item_api():
        payload = request.get_json(silent=True) or {}
        title = str(payload.get("title", "")).strip()
        details = str(payload.get("details", "")).strip()
        status = str(payload.get("status", "planned")).strip() or "planned"

        if not title or not details:
            return jsonify(error="title and details are required"), 400

        item = WorkItem(title=title, details=details, status=status)
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
