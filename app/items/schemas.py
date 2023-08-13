from pydantic import BaseModel


class ListItemModel(BaseModel):
    name: str
    price: float
