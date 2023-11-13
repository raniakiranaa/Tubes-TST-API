from pydantic import BaseModel

class Cart(BaseModel):
    id_cart: int        # an ID number
    username: str       # user using the cart
    status: str         # is available

    class Config:
        json_schema_extra = {
            "example": {
                "id_cart" : 3,
                "username" : "rerora",
                "status" : "false"
            }
        }

class Detail_cart(BaseModel):
    id_cartitem: int    # an ID number for each item in cart
    id_cart: int        # id cart for each detail
    id_product: int     # id product
    quantity: int       # quantity for each product

    class Config:
        schema_extra = {
            "example": {
                "id_cartitem" : 1,
                "id_cart" : 3,
                "id_product" : 1,
                "quantity" : 5
            }
        }