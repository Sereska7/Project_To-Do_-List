from fastapi import APIRouter, HTTPException, Depends

from core.exceptions.errors_task import TaskNotFound, NotOwnerError
from core.exceptions.general_errors import DataBaseError
from core.models.model_task import PermissionType
from core.schemas.schemas_task import TaskCreate, TaskRead
from core.schemas.schemas_user import UserRead
from core.dependencies.auth_depend import get_current_user
from crud.crud_task import task_create, get_tasks, update_task_with_permission_check, get_accessible_tasks
from crud.crud_task import get_task_by_id
from crud.crud_task import delete_task_by_id


router = APIRouter(tags=["Task"])


@router.post("/create_task")
async def create_task(
        task_in: TaskCreate,
        user: UserRead = Depends(get_current_user)
) -> TaskRead:
    try:
        new_task = await task_create(task_in, user)
        return new_task
    except DataBaseError:
        raise HTTPException(status_code=400, detail=f"Ошибка целостности данных.")


@router.get("/get_me_tasks")
async def get_me_task(
        user: UserRead = Depends(get_current_user)
) -> list[TaskRead]:
    tasks = await get_accessible_tasks(user.id, PermissionType.READ)
    return tasks


@router.get("/get_all_task")
async def get_all_task() -> list[TaskRead]:
    tasks = await get_tasks()
    return tasks


@router.patch("/update_task{task_id}")
async def update_task(
        task_id: int,
        task_in: TaskCreate,
        user: UserRead = Depends(get_current_user)
) -> TaskRead:
    task = await get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    up_task = await update_task_with_permission_check(user.id, task_id, task_in)
    return up_task


@router.delete("/delete_task{task_id}")
async def delete_task(
        task_id: int,
        user: UserRead = Depends(get_current_user)
) -> dict:
    try:
        task = await delete_task_by_id(task_id, user.id)
        return {"condition": True}
    except TaskNotFound:
        raise HTTPException(status_code=404, detail=f"Задача с id: {task_id} - не найдена")
    except NotOwnerError:
        raise HTTPException(status_code=404, detail="Пользователь не являеться создателем задачи")
