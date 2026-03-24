from flask import Blueprint, jsonify, request

from ..schemas import FIELD_SCHEMA, STATUSES
from ..services import WorkItemService, blueprint_metadata

api_bp = Blueprint("api", __name__)
service = WorkItemService()


@api_bp.get("/health")
def health():
    return jsonify(status="ok")


@api_bp.get("/schema")
def schema():
    meta = blueprint_metadata()
    return jsonify(meta)


@api_bp.get("/items")
def list_items():
    items = [item.to_dict() for item in service.list_items()]
    return jsonify(items)


@api_bp.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_item(
            title=payload.get("title", ""),
            status=payload.get("status", STATUSES[0]),
            payload=payload.get("payload", {}),
        )
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(item.to_dict()), 201


@api_bp.put("/items/<int:item_id>")
def update_item(item_id):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_item(
            item_id=item_id,
            title=payload.get("title", ""),
            status=payload.get("status", STATUSES[0]),
            payload=payload.get("payload", {}),
        )
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(item.to_dict())


@api_bp.delete("/items/<int:item_id>")
def delete_item(item_id):
    service.delete_item(item_id)
    return jsonify(status="deleted")


@api_bp.get("/metrics")
def metrics():
    return jsonify(service.metrics())
