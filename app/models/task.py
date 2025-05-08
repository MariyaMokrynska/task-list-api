from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id:
            result['goal_id'] = self.goal_id

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data["description"]
        )

    def update(self, source):
        self.title = source.title
        self.description = source.description
        self.completed_at = source.completed_at
