from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at is not None
        )

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at")
        )
