from enum import Enum

from pydantic import BaseModel

from items.schemas import MenuItem


class AddToCart(BaseModel):
    quantity: int = 1


class OptionName(str, Enum):
    incremente = "INC"
    decremente = "DEC"
    delete = "DEL"


class ChangeQuantity(BaseModel):
    status: OptionName
    name: str


class CartItem(BaseModel):
    name: str
    quantity: float
    price: float


class GetCart(BaseModel):
    cart_items: list[CartItem]
    final_value: float
