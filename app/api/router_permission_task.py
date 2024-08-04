from fastapi import APIRouter, Depends, HTTPException

from core.dependencies.auth_depend import get_current_user
from core.dependencies.permission_depend import verify_task_owner
from core.models.model_task import PermissionType
from core.schemas.schemas_permission import TaskPermissionResponse
from core.schemas.schemas_user import UserRead
from crud.crud_permission_task import grand_permission, revoke_permission

router = APIRouter(tags=["Permission"])


@router.post("/tasks/{task_id}/permissions")
async def add_permission(
    task_id: int,
    user_id: int,
    required_permission: PermissionType,
    current_user: UserRead = Depends(get_current_user),
) -> TaskPermissionResponse:
    task = await verify_task_owner(task_id, current_user.id)
    permission = await grand_permission(
        task_id, user_id, required_permission, current_user.id
    )
    if not permission:
        raise HTTPException(
            status_code=404, detail="Task not found or you are not the owner"
        )
    return permission


@router.delete("/tasks/{task_id}/permissions/{user_id}")
async def remove_permission(
    task_id: int,
    user_id: int,
    required_permission: PermissionType,
    current_user: UserRead = Depends(get_current_user),
) -> TaskPermissionResponse:
    task = await verify_task_owner(task_id, current_user.id)
    permission = await revoke_permission(
        task_id, user_id, required_permission, current_user.id
    )
    if not permission:
        raise HTTPException(
            status_code=404, detail="Task not found or you are not the owner"
        )
    return permission
