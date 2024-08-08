from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.core.base.db_helper import db_helper as db
from app.core.dependencies.auth_depend import get_current_user
from app.core.exceptions.errors_task import TaskNotFound, NotOwnerError
from app.core.models.model_task import Task
from app.core.exceptions.general_errors import DataBaseError


async def verify_task_owner(
    task_id: int, current_user_id: int = Depends(get_current_user)
):
    """
    Проверяет, является ли текущий пользователь владельцем задачи.

    Получает задачу по ID и проверяет, совпадает ли ID владельца задачи с ID текущего пользователя.
    Если задача не найдена или пользователь не является владельцем, выбрасывает HTTPException.
    """
    async with db.session_factory() as session:
        try:
            task = await session.get(Task, task_id)
            if not task:
                raise TaskNotFound(f"Task with id {task_id} not found")
            if task.user_id != current_user_id:
                raise NotOwnerError(
                    f"User with id {current_user_id} is not authorized to modify this task"
                )
        except IntegrityError:
            await session.rollback()
            raise DataBaseError(f"Ошибка базы данных")
