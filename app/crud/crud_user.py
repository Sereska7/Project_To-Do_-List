from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.models.model_user import User
from core.base.db_helper import db_helper as db
from core.exceptions.errors_user import UserAlreadyExists
from core.schemas.schemas_user import UserCreate, UserRead
from utils.func_by_auth import get_password_hash


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
        raise UserAlreadyExists(f"Польватель с таким email: {user_reg.email} уже существует")
    finally:
        await session.close()


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
