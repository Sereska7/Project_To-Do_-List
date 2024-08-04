import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.base.db_helper import db_helper
from api.router_user import router as router_user
from api.router_task import router as router_task
from api.router_permission_task import router as router_task_permission


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)


main_app.include_router(router_user)
main_app.include_router(router_task)
main_app.include_router(router_task_permission)


if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)
