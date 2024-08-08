from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.models.model_user import User
from app.core.base.db_helper import db_helper as db
from app.core.schemas.schemas_user import UserCreate, UserRead
from app.utils.func_by_auth import get_password_hash
from app.core.exceptions.general_errors import DataBaseError
from app.core.models.model_task import PermissionType, Task, TaskPermission
from app.core.exceptions.errors_user import UserHasNoPermission


async def create_user(user_reg: UserCreate) -> UserRead:
    """
    Создает нового пользователя.

    Принимает данные для регистрации пользователя, хеширует пароль,
    создает нового пользователя в базе данных и возвращает информацию о пользователе.
    """
    try:
        async with db.session_factory() as session:
            new_user = User(
                email=user_reg.email,
                hash_password=get_password_hash(user_reg.hash_password),
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
    except IntegrityError:
        await session.rollback()
        raise DataBaseError(f"Ошибка целостности данных.")


async def get_user_by_email(user_email: str) -> UserRead:
    async with db.session_factory() as session:
        request = select(User.__table__.columns).where(User.email == user_email)
        user = await session.execute(request)
        return user.mappings().one_or_none()


async def get_user_by_id(user_id: int) -> UserRead:
    async with db.session_factory() as session:
        request = select(User.__table__.columns).where(User.id == user_id)
        user = await session.execute(request)
        return user.mappings().one_or_none()


async def check_user_permission(
    user_id: int, task_id: int, permission: PermissionType
) -> bool:
    async with db.session_factory() as session:
        stmt = (
            select(Task)
            .outerjoin(TaskPermission, Task.id == TaskPermission.task_id)
            .filter(
                (Task.id == task_id)
                & (
                    (
                        (TaskPermission.user_id == user_id)
                        & (TaskPermission.permission == permission)
                    )
                    | (Task.user_id == user_id)
                )
            )
        )
        result = await session.execute(stmt)
        task = result.scalars().one_or_none()
        if not task:
            raise UserHasNoPermission("У пользователя нет прав доступа к задаче")
        return task
