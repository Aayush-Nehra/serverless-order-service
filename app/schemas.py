from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class OrderCreate(BaseModel):
    user_id: str
    amount: float


class OrderResponse(BaseModel):
    order_id: str
    user_id: str
    amount: float
    status: Literal["CREATED", "PAID", "SHIPPED"]
    created_at: datetime
