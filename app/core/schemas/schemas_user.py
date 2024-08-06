from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    hash_password: str


class UserCreate(BaseUser):
    pass


class UserRead(BaseModel):
    id: int
    email: EmailStr


class UserUpdate(BaseUser):
    pass
