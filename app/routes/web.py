from flask import Blueprint, Response, current_app, redirect, render_template, request, url_for

from ..schemas import FIELD_SCHEMA, STATUSES
from ..services import WorkItemService, blueprint_metadata

web_bp = Blueprint("web", __name__)
service = WorkItemService()


@web_bp.get("/")
def dashboard():
    items = service.list_items()
    metrics = service.metrics()
    return render_template(
        "index.html",
        items=items,
        metrics=metrics,
        field_schema=FIELD_SCHEMA,
        statuses=STATUSES,
        meta=blueprint_metadata(),
    )


@web_bp.route("/items/new", methods=["GET", "POST"])
def create_item():
    if request.method == "POST":
        payload = {field["key"]: request.form.get(field["key"], "") for field in FIELD_SCHEMA}
        try:
            service.create_item(
                title=request.form.get("title", ""),
                status=request.form.get("status", STATUSES[0]),
                payload=payload,
            )
            return redirect(url_for("web.dashboard"))
        except ValueError as exc:
            return render_template("form.html", error=str(exc), item=None, field_schema=FIELD_SCHEMA, statuses=STATUSES, meta=blueprint_metadata())
    return render_template("form.html", error=None, item=None, field_schema=FIELD_SCHEMA, statuses=STATUSES, meta=blueprint_metadata())


@web_bp.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    item = service.repo.get(item_id)
    if request.method == "POST":
        payload = {field["key"]: request.form.get(field["key"], "") for field in FIELD_SCHEMA}
        try:
            service.update_item(
                item_id=item_id,
                title=request.form.get("title", ""),
                status=request.form.get("status", STATUSES[0]),
                payload=payload,
            )
            return redirect(url_for("web.dashboard"))
        except ValueError as exc:
            return render_template("form.html", error=str(exc), item=item, field_schema=FIELD_SCHEMA, statuses=STATUSES, meta=blueprint_metadata())
    return render_template("form.html", error=None, item=item, field_schema=FIELD_SCHEMA, statuses=STATUSES, meta=blueprint_metadata())


@web_bp.post("/items/<int:item_id>/delete")
def delete_item(item_id):
    service.delete_item(item_id)
    return redirect(url_for("web.dashboard"))


@web_bp.get("/export.csv")
def export_csv():
    content = service.export_csv()
    return Response(
        content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )
