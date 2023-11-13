from fastapi import APIRouter, HTTPException, Query
from ..models.product import Product
from typing import Optional
from ..database.database import cursor, conn
from ..services.auth import user_dependency
from starlette import status

product_router = APIRouter(
    tags = ["Product"]
)

@product_router.get('/product')
async def retrieve_all_products():
    query = ("SELECT * FROM product")
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No product found")

@product_router.get('/product/{name_product}', response_model= str)
async def search_info_product(name_product: str):
    query = "SELECT * FROM product WHERE name = %s"
    cursor.execute(query, (name_product, ))
    result = cursor.fetchall()
    if result:
        aisle_name = result[0][6]
        response = f"{name_product} is in aisle {aisle_name}"

        for item in result:
            price = item[2]
            brand = item[3]
            stock = item[4]
            if stock > 0:
                response += f" {stock} items are available with brand {brand} for Rp.{price}\n"
            else:
                response += f" No stock available with brand {brand}"
        
        return response
    else:
        raise HTTPException(status_code=404, detail=f"No information found for product {name_product}")

@product_router.post("/product", response_model=str)
async def create_product(user: user_dependency, product: Product):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    if not product.name:
        raise HTTPException(status_code=422, detail=f"Product name is a required field. New product has not been added")
    if product.price < 0 or product.stock < 0:
        raise HTTPException(status_code=422, detail=f"Price and stock value should be at least 0. Product {product.name} has not been added")

    query = ("INSERT INTO product (name, price, brand, stock, category, aisle) VALUES (%s, %s, %s, %s, %s, %s)")
    values = (product.name, product.price, product.brand, product.stock, product.category, product.aisle)
    cursor.execute (query, values)
    conn.commit()
    return f"Product {product.name} has been added"

@product_router.put('/product/{id_product}', response_model= str)
async def update_product(user: user_dependency, id_product: int, price : Optional[int] = Query(0), stock : Optional[int] = Query(0)):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = "SELECT * FROM product WHERE id_product = %s"
    cursor.execute(query, (id_product, ))
    result = cursor.fetchall()
    if result:
        query = "UPDATE product SET stock = %s, price = %s WHERE id_product = %s"
        values = (stock, price, id_product)
        cursor.execute(query, values)
        conn.commit()
        return f"Product with id_product {id_product} has been updated"
    else:
        raise HTTPException(status_code=404, detail=f"No product found with id {id_product}")
    
@product_router.delete('/product/{id_product}', response_model= str)
async def delete_product(user: user_dependency, id_product: int):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = "SELECT * FROM product WHERE id_product = %s"
    cursor.execute(query, (id_product, ))
    result = cursor.fetchall()
    if result:
        query = "DELETE FROM product WHERE id_product = %s"
        cursor.execute(query, (id_product, ))
        conn.commit()
        return f"Product with id_product {id_product} has been deleted"
    else:
        raise HTTPException(status_code=404, detail=f"No product found with id_product {id_product}")