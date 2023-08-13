from enum import Enum

from pydantic import BaseModel


class AddToCart(BaseModel):
    quantity: int = 1


class OptionName(str, Enum):
    incremente = "INC"
    decremente = "DEC"
    delete = "DEL"


class ChangeQuantity(BaseModel):
    status: OptionName
    name: str
