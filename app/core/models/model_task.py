from datetime import date

from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, Integer, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from app.core.base.base_model import Base

if TYPE_CHECKING:
    from core.models.model_user import User


class PermissionType(Enum):
    READ = "read"
    UPDATE = "update"


class Task(Base):

    name_task: Mapped[str]
    description: Mapped[str]
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="task",
    )
    pr_task: Mapped["TaskPermission"] = relationship(
        "TaskPermission",
        uselist=False,
        back_populates="task_per",
        cascade='all, delete-orphan',
    )


class TaskPermission(Base):

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id", ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user_per: Mapped["User"] = relationship(back_populates="pr_task")
    task_per: Mapped["Task"] = relationship(back_populates="pr_task")

    permission: Mapped[PermissionType] = mapped_column(
        SQLEnum(PermissionType), nullable=False
    )

    __table_args__ = (
        UniqueConstraint('task_id', 'user_id', 'permission', name='uq_task_user_permission'),
    )
