from pydantic import BaseModel


class AddToCart(BaseModel):

    quantity:int =1