import asyncio
import json
from datetime import datetime

import pytest
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport

from core.config import settings
from app.core.base.base_model import Base
from app.core.base.db_helper import db_helper as db
from app.main import main_app as fastapi_app

from app.core.models.model_user import User
from app.core.models.model_task import Task, TaskPermission, PermissionType


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    user = open_mock_json("users")
    tasks = open_mock_json("tasks")
    permission = open_mock_json("permission_tasks")

    for task in tasks:
        task["date_from"] = datetime.strptime(task["date_from"], "%Y-%m-%d")
        task["date_to"] = datetime.strptime(task["date_to"], "%Y-%m-%d")
    for perm in permission:
        if perm["permission"] == "read":
            perm["permission"] = PermissionType.READ
        elif perm["permission"] == "update":
            perm["permission"] = PermissionType.UPDATE

    async with db.session_factory() as session:
        add_user = insert(User).values(user)
        add_task = insert(Task).values(tasks)
        add_permission_task = insert(TaskPermission).values(permission)

        await session.execute(add_user)
        await session.execute(add_task)
        await session.execute(add_permission_task)
        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac
