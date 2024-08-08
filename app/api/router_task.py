from fastapi import APIRouter, HTTPException, Depends

from app.core.exceptions.errors_task import TaskNotFound, NotOwnerError
from app.core.exceptions.general_errors import DataBaseError
from app.core.models.model_task import PermissionType
from app.core.schemas.schemas_task import TaskCreate, TaskRead
from app.core.schemas.schemas_user import UserRead
from app.core.dependencies.auth_depend import get_current_user
from app.crud.crud_task import (
    task_create,
    get_tasks,
    update_task_with_permission_check,
    get_accessible_task,
)
from app.crud.crud_task import get_task_by_id
from app.crud.crud_task import delete_task_by_id
from app.core.exceptions.errors_user import UserHasNoPermission

router = APIRouter(tags=["Task"])


@router.post("/create_task")
async def create_task(
    task_in: TaskCreate, user: UserRead = Depends(get_current_user)
) -> TaskRead:
    try:
        new_task = await task_create(task_in, user)
        return new_task
    except DataBaseError:
        raise HTTPException(status_code=400, detail=f"Ошибка целостности базы данных.")


@router.get("/get_me_tasks")
async def get_me_task(user: UserRead = Depends(get_current_user)) -> list[TaskRead]:
    tasks = await get_accessible_task(user.id, PermissionType.READ)
    return tasks


@router.get("/get_all_task")
async def get_all_task() -> list[TaskRead]:
    tasks = await get_tasks()
    return tasks


@router.patch("/update_task{task_id}")
async def update_task(
    task_id: int, task_in: TaskCreate, user: UserRead = Depends(get_current_user)
) -> TaskRead:
    try:
        task = await get_task_by_id(task_id)
        up_task = await update_task_with_permission_check(user.id, task_id, task_in)
        return up_task
    except UserHasNoPermission:
        raise HTTPException(
            status_code=400,
            detail=f"У пользователя нет прав на обновление задачи с id {task_id}.",
        )
    except TaskNotFound:
        raise HTTPException(
            status_code=404, detail=f"Задача с id {task_id} не найдена."
        )


@router.delete("/delete_task{task_id}")
async def delete_task(task_id: int, user: UserRead = Depends(get_current_user)) -> dict:
    try:
        task = await delete_task_by_id(task_id, user.id)
        return {"condition": True}
    except TaskNotFound:
        raise HTTPException(
            status_code=404, detail=f"Задача с id: {task_id} - не найдена"
        )
    except NotOwnerError:
        raise HTTPException(
            status_code=404, detail="Пользователь не являеться создателем задачи"
        )
    except DataBaseError:
        raise HTTPException(status_code=400, detail=f"Ошибка целостности базы данных.")
