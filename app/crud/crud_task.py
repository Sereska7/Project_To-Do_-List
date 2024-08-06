from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from core.base.db_helper import db_helper as db
from core.exceptions.errors_task import TaskNotFound, NotOwnerError
from core.exceptions.general_errors import DataBaseError
from core.models.model_task import Task, TaskPermission, PermissionType
from core.schemas.schemas_task import TaskCreate, TaskRead
from core.schemas.schemas_user import UserRead


async def task_create(
        task_in: TaskCreate,
        user: UserRead
) -> TaskRead:
    try:
        async with db.session_factory() as session:
            new_task = Task(
                name_task=task_in.name_task,
                description=task_in.description,
                date_from=task_in.date_from,
                date_to=task_in.date_to,
                user_id=user.id,
            )
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            return new_task
    except IntegrityError:
        await session.rollback()
        raise DataBaseError(f"Ошибка целостности данных.")
    finally:
        await session.close()


async def get_accessible_tasks(user_id: int, permission: PermissionType) -> list[TaskRead]:
    async with db.session_factory() as session:
        stmt = (
            select(Task)
            .outerjoin(TaskPermission, Task.id == TaskPermission.task_id)
            .filter(
                (TaskPermission.user_id == user_id)
                & (TaskPermission.permission == permission)
                | (Task.user_id == user_id))
            .options(
                joinedload(Task.pr_task)
            )  # Это загружает разрешения для каждой задачи
            .order_by(Task.id)
        )
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks


async def get_tasks() -> list[TaskRead]:
    async with db.session_factory() as session:
        tasks = await session.execute(select(Task.__table__.columns).order_by(Task.id))
        return tasks.mappings().all()


async def get_task_by_id(task_id: int):
    async with db.session_factory() as session:
        request = select(Task).where(Task.id == task_id)
        tasks = await session.execute(request)
        return tasks.one_or_none()


async def update_task_with_permission_check(
    user_id: int,
    task_id: int,
    task_update: TaskCreate,
) -> TaskRead:

    """Обновляет задачу после проверки прав доступа."""

    task = await get_accessible_tasks(user_id, PermissionType.UPDATE)
    if not task:
        raise TaskNotFound(f"Задача не найдена")
    async with db.session_factory() as session:
        # Обновление задачи
        request = (
            update(Task)
            .where(Task.id == task_id)
            .values(
                name_task=task_update.name_task,
                description=task_update.description,
                date_from=task_update.date_from,
                date_to=task_update.date_to,
            )
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(request)
        await session.commit()

        up_task = await session.execute(select(Task).where(Task.id == task_id))
        updated_task = up_task.scalar()

        if not updated_task:
            raise HTTPException(status_code=404, detail="Task is not found")

        return updated_task


async def delete_task_by_id(
        task_id: int,
        user_id: int
):
    """Удаляет задачу по её ID."""
    try:
        async with db.session_factory() as session:
            # Проверка наличия задачи
            task_stmt = select(Task).where(Task.id == task_id)
            task_result = await session.execute(task_stmt)
            task = task_result.scalars().first()

            if not task:
                raise TaskNotFound(f"Задача с id {task_id} не найдена")

            # Проверка прав доступа
            if task.user_id != user_id:
                raise NotOwnerError("Пользователь не является владельцем задачи.")

            # Выполнение запроса на удаление
            delete_stmt = delete(Task).where(Task.id == task_id)
            await session.execute(delete_stmt)
            await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка целостности базы данных")

