from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    hash_password: str


class UserCreate(BaseUser):
    pass


class UserRead(BaseUser):
    id: int
    email: EmailStr
    hash_password: str


class UserUpdate(BaseUser):
    pass
