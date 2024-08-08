from fastapi import APIRouter, HTTPException, Response

from app.core.dependencies.auth_depend import authenticate_user
from app.core.exceptions.errors_user import (
    UserAlreadyExists,
    UserNotFound,
    InvalidPasswordError,
)
from app.crud.crud_user import create_user, get_user_by_email
from app.core.schemas.schemas_user import UserCreate, UserRead
from app.utils.func_by_auth import create_access_token
from app.core.exceptions.general_errors import DataBaseError

router = APIRouter(tags=["Auth & User"])


@router.post("/register")
async def register_user(user_reg: UserCreate) -> UserRead:
    try:
        user = await get_user_by_email(user_reg.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким адресом электронной почты уже существует",
            )
        new_user = await create_user(user_reg)
        return new_user
    except UserAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким адресом электронной почты уже существует",
        )
    except DataBaseError:
        raise HTTPException(status_code=400, detail=f"Ошибка целостности базы данных.")


@router.post("/login")
async def login_user(response: Response, user_data: UserCreate) -> dict:
    try:
        user = await authenticate_user(user_data.email, user_data.hash_password)
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("access_token", access_token, httponly=True)
        return {"access_token": "Пользователь аутентифицирован"}
    except UserNotFound:
        raise HTTPException(
            status_code=404, detail=f"Пользователь с email: {user_data.email} не найден"
        )
    except InvalidPasswordError:
        raise HTTPException(status_code=400, detail=f"Пароль не верный.")
    except Exception:
        raise HTTPException(status_code=500, detail="Произошла непредвиденная ошибка")


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"access": "Delete cookies"}
