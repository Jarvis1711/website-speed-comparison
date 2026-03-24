from io import StringIO
import csv

from .repositories import WorkItemRepository
from .schemas import FIELD_SCHEMA, STATUSES, validate_payload


class WorkItemService:
    def __init__(self):
        self.repo = WorkItemRepository()

    def list_items(self):
        return self.repo.list_all()

    def metrics(self):
        items = self.repo.list_all()
        status_counts = {status: 0 for status in STATUSES}
        for item in items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
        return {"total": len(items), "by_status": status_counts}

    def create_item(self, title, status, payload):
        title = (title or "").strip()
        if not title:
            raise ValueError("title is required")
        selected_status = status if status in STATUSES else STATUSES[0]
        cleaned = validate_payload(payload)
        return self.repo.create(title=title, status=selected_status, payload=cleaned)

    def update_item(self, item_id, title, status, payload):
        item = self.repo.get(item_id)
        title = (title or "").strip()
        if not title:
            raise ValueError("title is required")
        selected_status = status if status in STATUSES else STATUSES[0]
        cleaned = validate_payload(payload)
        return self.repo.update(item=item, title=title, status=selected_status, payload=cleaned)

    def delete_item(self, item_id):
        item = self.repo.get(item_id)
        self.repo.delete(item)

    def export_csv(self):
        rows = self.repo.list_all()
        buffer = StringIO()
        writer = csv.writer(buffer)
        columns = ["id", "title", "status", "created_at", "updated_at"] + [field["key"] for field in FIELD_SCHEMA]
        writer.writerow(columns)
        for row in rows:
            payload_cells = [row.payload.get(field["key"], "") for field in FIELD_SCHEMA]
            writer.writerow([row.id, row.title, row.status, row.created_at.isoformat(), row.updated_at.isoformat(), *payload_cells])
        return buffer.getvalue()


def blueprint_metadata():
    return {
        "domain": "Developer Experience",
        "entity": "Engineering Initiative",
        "entity_plural": "Engineering Initiatives",
        "statuses": STATUSES,
        "fields": FIELD_SCHEMA,
    }
