from pydantic import BaseModel
from typing import Union

class ItemPrice(BaseModel):
    name: str
    buy: float
    sell: Union[float, None]
    limits: Union[str, None]