from fastapi import APIRouter, Depends, HTTPException

from core.dependencies.auth_depend import get_current_user
from core.dependencies.permission_depend import verify_task_owner
from core.exceptions.errors_permission_task import PermissionAlreadyExists, PermissionNotFound
from core.exceptions.errors_task import NotOwnerError, TaskNotFound
from core.exceptions.general_errors import DataBaseError
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
    try:
        task = await verify_task_owner(task_id, current_user.id)
        permission = await grand_permission(
            task_id,
            user_id,
            required_permission,
            current_user.id
        )
        return permission
    except NotOwnerError:
        raise HTTPException(status_code=404, detail="Пользователь не являеться создателем задачи")
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    except PermissionAlreadyExists:
        raise HTTPException(
            status_code=404, detail="Права доступа уже выданы пользователю"
        )


@router.delete("/tasks/{task_id}/permissions/{user_id}")
async def remove_permission(
    task_id: int,
    user_id: int,
    required_permission: PermissionType,
    current_user: UserRead = Depends(get_current_user),
) -> TaskPermissionResponse:
    try:
        task = await verify_task_owner(task_id, current_user.id)
        permission = await revoke_permission(
            task_id,
            user_id,
            required_permission,
            current_user.id
        )
        return permission
    except NotOwnerError:
        raise HTTPException(status_code=404, detail="Пользователь не являеться создателем задачи")
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    except DataBaseError:
        raise HTTPException(status_code=400, detail="Ошибка целостности базы данных")
    except PermissionNotFound:
        raise HTTPException(status_code=404,
                            detail=f"Разрешение для task_id {task_id}"
                                   f"и user_id {user_id} не найдено")

