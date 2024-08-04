from fastapi import HTTPException, Depends, Request
from jose import jwt, ExpiredSignatureError, JWTError
from pydantic import EmailStr

from app.core.config import settings
from crud.crud_user import get_user_by_id, get_user_by_email
from utils.func_by_auth import verify_password


async def authenticate_user(email: EmailStr, password: str):
    """
    Аутентификация пользователя.

    Проверяет наличие пользователя с указанным email и соответствие пароля.
    Если пользователь не найден или пароль не совпадает, выбрасывает HTTPException.
    """
    user = await get_user_by_email(email)
    if not (user and verify_password(password, user.hash_password)):
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_token(request: Request):
    """
    Извлечение токена из cookies запроса.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=500, detail="Not token")
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
        raise HTTPException(status_code=500, detail="ExpiredSignatureError")
    except JWTError:
        raise HTTPException(status_code=500, detail="JWTError")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=404, detail="User_id not found")
    user = await get_user_by_id(user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
