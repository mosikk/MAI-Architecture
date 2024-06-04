from pydantic import BaseModel


class Task(BaseModel):
    id: int
    task_name: str
    description: str
    executor_name: str


class UpdateTask(BaseModel):
    task_name: str
    description: str
    executor_name: str
