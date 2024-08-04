from pydantic import BaseModel


class TaskPermissionCreate(BaseModel):
    user_id: int
    permission: str


class TaskPermissionResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    permission: str
