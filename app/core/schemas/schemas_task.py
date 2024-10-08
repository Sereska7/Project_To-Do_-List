from datetime import date

from pydantic import BaseModel, ConfigDict


class BaseTask(BaseModel):
    name_task: str
    description: str
    date_from: date
    date_to: date


class TaskCreate(BaseTask):
    pass


class TaskRead(BaseModel):
    id: int
    name_task: str
    description: str
    date_from: date
    date_to: date
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseTask):
    pass
