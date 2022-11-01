from pydantic import BaseModel

from datetime import datetime
from typing import List


class ShopItem(BaseModel):
    id : int
    name: str
    price: float
    added_time: datetime
    updated_time: datetime
    category_id: int

    class Config:
        orm_mode = True


class CreateShopItem(BaseModel):
    name: str
    price: float
    category_id: int




