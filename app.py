from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

FIELD_SCHEMA = [
  {
    "key": "repository",
    "label": "Repository",
    "input_type": "text",
    "required": true
  },
  {
    "key": "impact_score",
    "label": "Impact Score",
    "input_type": "number",
    "required": true
  },
  {
    "key": "technical_notes",
    "label": "Technical Notes",
    "input_type": "textarea",
    "required": true
  }
]
STATUSES = ["captured", "implementing", "review", "released"]


class DomainRecord(db.Model):
    __tablename__ = "domain_records"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(40), nullable=False, default=STATUSES[0])
    payload = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


def _parse_payload(form_or_json):
    payload = {}
    for field in FIELD_SCHEMA:
        raw = form_or_json.get(field["key"], "")
        if isinstance(raw, str):
            raw = raw.strip()
        if field["required"] and (raw is None or raw == ""):
            raise ValueError(f"{field['label']} is required")
        if field["input_type"] == "number" and raw not in ("", None):
            try:
                raw = float(raw)
            except ValueError as exc:
                raise ValueError(f"{field['label']} must be numeric") from exc
        payload[field["key"]] = raw
    return payload


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        APP_TITLE="Website Speed Comparison",
        APP_DESCRIPTION="Production-ready domain application.",
        DOMAIN_LABEL="Developer Experience",
        ENTITY_SINGULAR="Website Speed Engineering Item",
        ENTITY_PLURAL="Website Speed Engineering Items",
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.get("/")
    def dashboard():
        records = DomainRecord.query.order_by(DomainRecord.updated_at.desc()).all()
        counts = {status: DomainRecord.query.filter_by(status=status).count() for status in STATUSES}
        return render_template(
            "index.html",
            records=records,
            counts=counts,
            field_schema=FIELD_SCHEMA,
            statuses=STATUSES,
        )

    @app.route("/records/new", methods=["GET", "POST"])
    def create_record():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            status = request.form.get("status", STATUSES[0]).strip() or STATUSES[0]
            try:
                payload = _parse_payload(request.form)
            except ValueError as exc:
                return render_template("form.html", record=None, statuses=STATUSES, field_schema=FIELD_SCHEMA, error=str(exc))
            if not title:
                return render_template("form.html", record=None, statuses=STATUSES, field_schema=FIELD_SCHEMA, error="Title is required")
            record = DomainRecord(title=title, status=status, payload=payload)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("form.html", record=None, statuses=STATUSES, field_schema=FIELD_SCHEMA, error=None)

    @app.route("/records/<int:record_id>/edit", methods=["GET", "POST"])
    def edit_record(record_id):
        record = DomainRecord.query.get_or_404(record_id)
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            status = request.form.get("status", STATUSES[0]).strip() or STATUSES[0]
            try:
                payload = _parse_payload(request.form)
            except ValueError as exc:
                return render_template("form.html", record=record, statuses=STATUSES, field_schema=FIELD_SCHEMA, error=str(exc))
            if not title:
                return render_template("form.html", record=record, statuses=STATUSES, field_schema=FIELD_SCHEMA, error="Title is required")
            record.title = title
            record.status = status
            record.payload = payload
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("form.html", record=record, statuses=STATUSES, field_schema=FIELD_SCHEMA, error=None)

    @app.post("/records/<int:record_id>/delete")
    def delete_record(record_id):
        record = DomainRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", app=app.config["APP_TITLE"], domain=app.config["DOMAIN_LABEL"])

    @app.get("/api/schema")
    def schema():
        return jsonify(statuses=STATUSES, fields=FIELD_SCHEMA)

    @app.get("/api/records")
    def list_records():
        records = DomainRecord.query.order_by(DomainRecord.updated_at.desc()).all()
        return jsonify([record.to_dict() for record in records])

    @app.post("/api/records")
    def create_record_api():
        payload_raw = request.get_json(silent=True) or {}
        title = str(payload_raw.get("title", "")).strip()
        status = str(payload_raw.get("status", STATUSES[0])).strip() or STATUSES[0]
        data = payload_raw.get("payload", {})
        if not isinstance(data, dict):
            return jsonify(error="payload must be an object"), 400
        try:
            payload = _parse_payload(data)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        if not title:
            return jsonify(error="title is required"), 400
        record = DomainRecord(title=title, status=status, payload=payload)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201

    @app.get("/api/metrics")
    def metrics():
        by_status = {status: DomainRecord.query.filter_by(status=status).count() for status in STATUSES}
        return jsonify(total=sum(by_status.values()), by_status=by_status)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
