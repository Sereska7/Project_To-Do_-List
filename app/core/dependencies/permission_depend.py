from fastapi import Depends, HTTPException

from core.base.db_helper import db_helper as db
from core.dependencies.auth_depend import get_current_user
from core.models.model_task import Task


async def verify_task_owner(
    task_id: int, current_user_id: int = Depends(get_current_user)
):
    """
    Проверяет, является ли текущий пользователь владельцем задачи.

    Получает задачу по ID и проверяет, совпадает ли ID владельца задачи с ID текущего пользователя.
    Если задача не найдена или пользователь не является владельцем, выбрасывает HTTPException.
    """
    async with db.session_factory() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to modify this task"
            )
        return task
