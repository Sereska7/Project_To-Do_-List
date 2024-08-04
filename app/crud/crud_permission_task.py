from fastapi import HTTPException
from sqlalchemy import select, and_

from core.base.db_helper import db_helper as db
from core.models.model_task import TaskPermission, PermissionType
from core.schemas.schemas_permission import TaskPermissionResponse


async def grand_permission(
    task_id: int, user_id: int, required_permission: PermissionType, owner_id: int
) -> TaskPermissionResponse:
    """
    Предоставляет разрешение пользователю на указанную задачу.

    Проверяет, существует ли уже разрешение для данной задачи и пользователя.
    Если разрешения нет, создает новое. Если разрешение уже существует, выбрасывает HTTPException.
    """
    async with db.session_factory() as session:
        stml = select(TaskPermission).filter(
            and_(
                TaskPermission.task_id == task_id,
                TaskPermission.user_id == user_id,
                TaskPermission.permission == required_permission.name,
            )
        )
        result = await session.execute(stml)
        have_permission = result.scalar_one_or_none()
        if not have_permission:
            permission = TaskPermission(
                task_id=task_id, user_id=user_id, permission=required_permission
            )
            session.add(permission)
            await session.commit()
            await session.refresh(permission)
            return permission
        else:
            raise HTTPException(status_code=404, detail="Permission already exists")


async def revoke_permission(
    task_id: int, user_id: int, required_permission: PermissionType, owner_id: int
) -> TaskPermissionResponse:
    """
    Отзывает разрешения у пользователя на указанную задачу.

    Проверяет наличие разрешения для данной задачи и пользователя.
    Если разрешение существует, удаляет его. Если разрешение не найдено, возвращает None.
    """
    async with db.session_factory() as session:
        request = select(TaskPermission).filter(
            TaskPermission.task_id == task_id,
            TaskPermission.user_id == user_id,
            TaskPermission.permission == required_permission,
        )
        result = await session.execute(request)
        permission = result.scalar_one_or_none()
        if not permission:
            return None

        await session.delete(permission)
        await session.commit()
        return permission
