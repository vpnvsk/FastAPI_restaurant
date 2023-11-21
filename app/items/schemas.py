from pydantic import BaseModel


class ListItemModel(BaseModel):
    name: str
    price: float


class MenuItem(BaseModel):
    name: str
    price: float
    ingridients: str
