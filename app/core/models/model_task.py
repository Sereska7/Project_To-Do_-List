from datetime import date

from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, Integer, Enum as SQLEnum
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="task")
    pr_task: Mapped["TaskPermission"] = relationship(
        "TaskPermission", back_populates="task_per"
    )


class TaskPermission(Base):
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user_per: Mapped["User"] = relationship(back_populates="pr_task")
    task_per: Mapped["Task"] = relationship(back_populates="pr_task")

    permission: Mapped[PermissionType] = mapped_column(
        SQLEnum(PermissionType), nullable=False
    )
