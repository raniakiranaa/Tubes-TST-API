from fastapi import APIRouter, HTTPException, Query
from app.models.product import Product
from typing import Optional
from app.database.database import cursor, conn
from app.utils.auth import user_dependency
from starlette import status

product_router = APIRouter(
    tags = ["Product"]
)

@product_router.get('/product')
async def retrieve_all_products(user: user_dependency):
    query = ("SELECT * FROM product WHERE store_id = %s")
    cursor.execute(query, (user[4], ))
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No product found")

@product_router.get('/product/{name_product}', response_model= str)
async def search_info_product(user: user_dependency, name_product: str):
    query = "SELECT * FROM product WHERE store_id = %s and name = %s"
    values = (user[4], name_product)
    cursor.execute(query, values)
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
async def create_product(user: user_dependency, name: str, price: int, brand: str, stock: int, category: str, aisle: str):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    if not name:
        raise HTTPException(status_code=422, detail=f"Product name is a required field. New product has not been added")
    if price < 0 or stock < 0:
        raise HTTPException(status_code=422, detail=f"Price and stock value should be at least 0. Product {name} has not been added")

    query = ("INSERT INTO product (name, price, brand, stock, category, aisle, store_id) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    values = (name, price, brand, stock, category, aisle, user[4])
    cursor.execute (query, values)
    conn.commit()
    return f"Product {name} has been added"

@product_router.put('/product/{id_product}', response_model= str)
async def update_product(user: user_dependency, id_product: int, price : Optional[int] = Query(0), stock : Optional[int] = Query(0)):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = "SELECT * FROM product WHERE store_id = %s AND id_product = %s"
    values = (user[4], id_product)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if result:
        query = "UPDATE product SET stock = %s, price = %s WHERE store_id = %s AND id_product = %s"
        values = (stock, price, user[4], id_product)
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

    query = "SELECT * FROM product WHERE store_id = %s AND id_product = %s"
    values = (user[4], id_product)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if result:
        query = "DELETE FROM product WHERE store_id = %s AND id_product = %s"
        values = (user[4], id_product)
        cursor.execute(query, values)
        conn.commit()
        return f"Product with id_product {id_product} has been deleted"
    else:
        raise HTTPException(status_code=404, detail=f"No product found with id_product {id_product}")