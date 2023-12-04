from pydantic import BaseModel

class Product(BaseModel):
    id_product: int     # an ID number
    name: str           # product name
    price: int          # product price
    brand: str          # product brand
    stock: int          # product stock
    category: str       # product category 
    aisle: str          # product aisle
    store_id: str       # product store

    class Config:
        json_schema_extra = {
            "example": {
                "id_product" : 1,
                "name": "Pensil",
                "price": 1500,
                "brand": "Faber-Castell",
                "stock" : 10,
                "category" : "Alat Tulis",
                "aisle" : "Stationary",
                "store_id" : "A"
            }
        }