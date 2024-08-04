from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from app.core.base.base_model import Base

if TYPE_CHECKING:
    from core.models.model_task import Task, TaskPermission


class User(Base):

    email: Mapped[str] = mapped_column(String, unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))

    task: Mapped["Task"] = relationship("Task", back_populates="user")
    pr_task: Mapped["TaskPermission"] = relationship(
        "TaskPermission", back_populates="user_per"
    )
