from pydantic import BaseModel


class Order(BaseModel):
    id: int
    user_id: int
    tasks_id: int
    status: str


class UpdateOrder(BaseModel):
    user_id: int
    tasks_id: int
    status: str
