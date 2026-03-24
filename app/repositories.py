from . import db
from .models import WorkItem


class WorkItemRepository:
    def list_all(self):
        return WorkItem.query.order_by(WorkItem.updated_at.desc()).all()

    def get(self, item_id):
        return WorkItem.query.get_or_404(item_id)

    def create(self, title, status, payload):
        item = WorkItem(title=title, status=status, payload=payload)
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, item, title, status, payload):
        item.title = title
        item.status = status
        item.payload = payload
        db.session.commit()
        return item

    def delete(self, item):
        db.session.delete(item)
        db.session.commit()
