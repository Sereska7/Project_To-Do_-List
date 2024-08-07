from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.base.db_helper import db_helper as db
from app.core.exceptions.errors_permission_task import PermissionAlreadyExists, PermissionNotFound
from app.core.exceptions.general_errors import DataBaseError
from app.core.models.model_task import TaskPermission, PermissionType
from app.core.schemas.schemas_permission import TaskPermissionResponse


async def get_permission(
        task_id: int,
        user_id: int,
        required_permission: PermissionType,
        owner_id: int
) -> TaskPermissionResponse:
    try:
        async with db.session_factory() as session:
            requery = select(TaskPermission).where(
                TaskPermission.task_id == task_id,
                TaskPermission.user_id == user_id,
                TaskPermission.permission == required_permission
            )
            permission = await session.execute(requery)
            return permission.scalar_one_or_none()
    except IntegrityError:
        await session.rollback()
        raise DataBaseError("Ошибка целостности базы данных")


async def grand_permission(
    task_id: int, user_id: int, required_permission: PermissionType, owner_id: int
) -> TaskPermissionResponse:
    """
    Предоставляет разрешение пользователю на указанную задачу.

    Проверяет, существует ли уже разрешение для данной задачи и пользователя.
    Если разрешения нет, создает новое. Если разрешение уже существует, выбрасывает HTTPException.
    """
    async with db.session_factory() as session:
        try:
            task_permission = TaskPermission(
                task_id=task_id,
                user_id=user_id,
                permission=required_permission
            )
            session.add(task_permission)
            await session.commit()
            await session.refresh(task_permission)
            return task_permission
        except IntegrityError:
            await session.rollback()
            raise PermissionAlreadyExists(f"Разрешение: {required_permission},"
                                          f"для пользователя: {user_id} уже существует.")


async def revoke_permission(
    task_id: int, user_id: int, required_permission: PermissionType, owner_id: int
) -> TaskPermissionResponse:
    """
    Отзывает разрешения у пользователя на указанную задачу.

    Проверяет наличие разрешения для данной задачи и пользователя.
    Если разрешение существует, удаляет его. Если разрешение не найдено, возвращает None.
    """
    try:
        async with db.session_factory() as session:
            # Проверка наличия разрешения
            request = select(TaskPermission).filter(
                TaskPermission.task_id == task_id,
                TaskPermission.user_id == user_id,
                TaskPermission.permission == required_permission,
            )
            result = await session.execute(request)
            permission = result.scalar_one_or_none()

            if permission is None:
                raise PermissionNotFound(f"Разрешение для task_id {task_id} и user_id {user_id} не найдено")

            # Удаление разрешения
            await session.delete(permission)
            await session.commit()
            return permission
    except IntegrityError:
        await session.rollback()
        raise DataBaseError("Ошибка целостности базы данных")
