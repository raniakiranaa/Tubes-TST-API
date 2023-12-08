from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    id_transaction: int                 # an ID number
    store_id: str                       # store transaction
    date: datetime                      # transaction date and time
    total_price: int                    # transaction total price

    class Config:
        json_schema_extra = {
            "example": {
                "id_transaction" : 1,
                "store_id" : "A",
                "date": "2023-11-06 05:15:56",
                "total_price": 316500
            }
        }

class Detail_transaction(BaseModel):
    id_transactionitem: int     # an ID number for each item in transaction
    id_transaction: int         # id transaction for each detail
    store_id: str               # id store
    id_product: int             # id product
    quantity: int               # quantity for each product

    class Config:
        schema_extra = {
            "example" : {
                "id_transactionitem" : 1,
                "id_transaction" : 1,
                "store_id" : "A",
                "id_product" : 1,
                "quantity" : 5
            }
        }