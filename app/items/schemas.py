from pydantic import BaseModel
from typing import List, Dict


# class ItemCreate(BaseModel):
#     id: int
#     name: str
#     ingridient: str
#     category_id: int
#     price: int

class ListItemModel(BaseModel):
    name: str
    price: float

# class CategoryItemsModel(BaseModel):
#     __root__: Dict[str, List[ListItemModel]]