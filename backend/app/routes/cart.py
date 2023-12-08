from fastapi import APIRouter, HTTPException
from app.models.cart import Cart, Detail_cart
from app.database.database import cursor, conn
from app.utils.auth import user_dependency

cart_router = APIRouter(
    tags = ["Cart"]
)

def get_user_cart(user: user_dependency):
    query = ("SELECT id_cart FROM cart WHERE username = %s")
    cursor.execute(query, (user[0], ))
    user_cart = cursor.fetchone()
    return user_cart

@cart_router.get('/cart')
async def get_info_cart(user: user_dependency):
    user_cart = get_user_cart(user)
    if user_cart is None:
        raise HTTPException(status_code=422, detail=f"Please assign user to cart")
    else:
        query = ("SELECT * FROM detail_cart where id_cart = %s")
        cursor.execute(query, (user_cart[0], ))
        result = cursor.fetchall()
        if result:
            # calculate total price
            total_price = 0
            for item in result:
                query = ("SELECT price FROM product WHERE id_product = %s")
                cursor.execute(query, (item[2], ))
                price = cursor.fetchone()
                total_price += item[3] * price[0]
            response = result
            response.append({f"Total price in cart is {total_price}"})
            return result
        else:
            raise HTTPException(status_code=404, detail=f"No product found in cart with id {user_cart[0]}")

@cart_router.put('/cart')
async def assign_cart(user: user_dependency):
    user_cart = get_user_cart(user)
    if user_cart is None:
        # true if a user already have the cart, false if not
        query = ("SELECT * FROM cart WHERE store_id = %s AND status = 'True'")
        cursor.execute(query, (user[4], ))
        result =  cursor.fetchall()
        if result:
            query = ("UPDATE cart SET username = %s, status = 'false' WHERE id_cart = %s")
            values = (user[0], result[0][0])
            cursor.execute(query, values)
            conn.commit()
            return f"User {user[0]} is using cart with id {result[0][0]}"
        else:
            # all cart is occupied
            raise HTTPException(status_code=404, detail=f"No empty cart is found. Sorry :(")
    else:
        raise HTTPException(status_code=422, detail=f"User is already assigned to cart with id {user_cart[0]}")

@cart_router.post('/detail_cart')
async def add_item_to_cart(user: user_dependency, id_product: int, addClick: bool):
    user_cart = get_user_cart(user)
    if user_cart is None:
        raise HTTPException(status_code=422, detail=f"Please assign cart to user {user[0]}")
    
    # validasi product
    query = ("SELECT * FROM product WHERE store_id = %s AND id_product = %s")
    values = (user[4], id_product)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        if addClick:
            # add 1 item
            query = ("SELECT * FROM detail_cart WHERE id_cart = %s and id_product = %s")
            cursor.execute(query, (user_cart[0], id_product, ))
            result = cursor.fetchall()
            if result:
                # product in cart
                query = ("UPDATE detail_cart SET quantity = quantity + 1 WHERE id_cart = %s AND id_product = %s")
                values = (user_cart[0], id_product)
                cursor.execute(query, values)
                conn.commit()
            else:
                # product not in cart
                query = ("INSERT INTO detail_cart (id_cart, id_product, quantity) VALUES (%s, %s, 1)")
                values = (user_cart[0], id_product)
                cursor.execute(query, values)
                conn.commit()

            return f"Product with id {id_product} has been added to cart"
        else:
            # delete 1 item
            query = ("SELECT * FROM detail_cart WHERE id_cart = %s and id_product = %s")
            values = (user_cart[0], id_product)
            cursor.execute(query, values)
            result = cursor.fetchall()
            if result:
                # product in cart
                query = ("SELECT quantity FROM detail_cart WHERE id_cart = %s AND id_product = %s")
                values = (user_cart[0], id_product)
                cursor.execute(query, values)
                result = cursor.fetchone()
                if result[0] != 1:
                    query = ("UPDATE detail_cart SET quantity = quantity - 1 WHERE id_cart = %s AND id_product = %s")
                    values = (user_cart[0], id_product)
                    cursor.execute(query, values)
                    conn.commit()
                else:
                    query = ("DELETE FROM detail_cart WHERE id_cart = %s AND id_product = %s")
                    values = (user_cart[0], id_product)
                    cursor.execute(query, values)
                    conn.commit()
                return f"Cart has been updated"
            else:
                # product not in cart
                raise HTTPException(status_code=404, detail=f"No product found under id {id_product}")

    else:
        raise HTTPException(status_code=404, detail=f"No product found under id {id_product}")
    
@cart_router.delete('/cart')
async def delete_user_cart(user: user_dependency):
    user_cart = get_user_cart(user)
    # get current user
    if user_cart is None:
        raise HTTPException(status_code=422, detail=f"No cart assigned to user found")
    else:
        # delete item in cart
        delete_done_cart(user_cart[0])

        # change cart to inactive
        query = "UPDATE cart SET status = 'true', username = Null WHERE id_cart = %s"
        cursor.execute(query, (user_cart[0], ))
        conn.commit()
        return f"Cart has been emptied and reassigned"

def delete_done_cart(user_cart: int):
    query = "DELETE FROM detail_cart where id_cart = %s"
    cursor.execute(query, (user_cart, ))
    conn.commit()
