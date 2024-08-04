from fastapi import APIRouter, HTTPException, Response

from core.dependencies.auth_depend import authenticate_user
from crud.crud_user import create_user, get_user_by_email
from core.schemas.schemas_user import UserCreate, UserRead
from utils.func_by_auth import create_access_token

router = APIRouter(tags=["Auth & User"])


@router.post("/register")
async def register_user(user_reg: UserCreate) -> UserRead:
    user = await get_user_by_email(user_reg.email)
    if user:
        raise HTTPException(status_code=401, detail="User already exists")
    return await create_user(user_reg)


@router.post("/login")
async def login_user(response: Response, user_data: UserCreate) -> dict:
    user = await authenticate_user(user_data.email, user_data.hash_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"access": "True"}
