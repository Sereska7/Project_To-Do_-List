from fastapi import HTTPException, Depends, Request
from jose import jwt, ExpiredSignatureError, JWTError
from pydantic import EmailStr

from app.core.config import settings
from app.core.exceptions.errors_user import UserNotFound, InvalidPasswordError, TokenNotFound
from app.crud.crud_user import get_user_by_id, get_user_by_email
from app.utils.func_by_auth import verify_password


async def authenticate_user(email: EmailStr, password: str):
    """
    Аутентификация пользователя.

    Проверяет наличие пользователя с указанным email и соответствие пароля.
    """
    user = await get_user_by_email(email)
    if not user:
        raise UserNotFound(f"Пользователь с email: {email} не найден")
    else:
        if not verify_password(password, user.hash_password):
            raise InvalidPasswordError("Пароль не верный.")
    return user


def get_token(request: Request):
    """
    Извлечение токена из cookies запроса.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise TokenNotFound(f"Токен пользователя не найден")
    return token


async def get_current_user(token: str = Depends(get_token)):
    """
    Получает текущего пользователя по JWT-токену.

    Декодирует токен, проверяет его валидность и извлекает ID пользователя.
    Если токен недействителен или пользователь не найден, выбрасывает HTTPException.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=500, detail="Срок действия токена истек.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Произошла непредвиденная ошибка.")
    user = await get_user_by_id(user_id=int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    return user
