from fastapi import APIRouter, HTTPException, Query
from app.models.transaction import Transaction, Detail_transaction
from typing import Optional
from app.database.database import cursor, conn
from collections import defaultdict, Counter
from app.utils.auth import user_dependency
from app.routes.cart import get_user_cart, delete_user_cart,get_info_cart

transaction_router = APIRouter(
    tags = ["Transaction"]
)

@transaction_router.get('/transaction/{username}')
async def get_transaction(user: user_dependency):
    query = ("SELECT * FROM transaction WHERE username = %s")
    cursor.execute(query, (user[0], ))
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No transaction found for user {user[0]}")

@transaction_router.get('/detail_transaction/')
async def get_information_transaction(user: user_dependency, name_product: Optional[str] = Query(None)):
    if name_product:
        query = "SELECT * FROM product WHERE store_id = %s AND name LIKE CONCAT ('%', %s, '%')"
        values = (user[4], name_product)
        cursor.execute(query, values)
        result = cursor.fetchall()
        if result:
            query = "SELECT name, brand, SUM(quantity) as total FROM detail_transaction JOIN product ON detail_transaction.id_product = product.id_product WHERE detail_transaction.store_id = %s AND name = %s GROUP BY name, brand ORDER BY total DESC"
            values = (user[4], name_product)
            cursor.execute(query, values)
            result = cursor.fetchall()

            if result:
                fav_merk = result[0][1]
                return f"The most bought brand for product {name_product} is {fav_merk}"
            else:
                raise HTTPException(status_code=404, detail=f"No transaction found for product: {name_product}")
        else:
            raise HTTPException(status_code=404, detail=f"No product found with name = {name_product}")
    else:
        query = ("SELECT * FROM detail_transaction where store_id = %s")
        cursor.execute(query, (user[4], ))
        result = cursor.fetchall()
        return result
    
@transaction_router.get('/detail_transaction/{id_product}')
async def product_recommendation(user: user_dependency, id_product: int):
    query = "SELECT name FROM product WHERE store_id = %s AND id_product = %s"
    values = (user[4], id_product)
    cursor.execute(query, values)
    name = cursor.fetchone()
    if name:
        query = "SELECT id_transaction, id_product FROM detail_transaction"
        cursor.execute(query)
        result = cursor.fetchall()

        transaction_data = defaultdict(list)
        for item in result:
            id_transaction, id_item = item
            transaction_data[id_transaction].append(id_item)
        
        result = [tuple(trans) for trans in transaction_data.values()]
        related_transactions = [transaction for transaction in result if id_product in transaction]
        items = [item for transaction in related_transactions for item in transaction if item != id_product]

        counter = Counter(items)
        most_common = counter.most_common()
        list_item = []
        for item in most_common:
            query = "SELECT name FROM product WHERE id_product = %s"
            cursor.execute(query, (item[0],))
            item_name = cursor.fetchone()
            if item_name and item_name != name:
                list_item.append(item_name)

        list_frequent = list(set(list_item))[:3]
        list_new = [item[0] for item in list_frequent]
        if list_new:
            return f"Product frequently bought with {name[0]}: {list_new}"
        else:
            return "We have no information on this. Be the first to try it out!"
        
    else:
        raise HTTPException(status_code=404, detail=f"No information found for product with ID = {id_product}")

# transaction done -> add id transaction -> add detail -> delete detail cart -> delete id cart
@transaction_router.post('/transaction')
async def create_transaction(user: user_dependency):
    user_cart = get_user_cart(user)
    if user_cart is None:
        raise HTTPException(status_code=422, detail=f"Please assign cart to user {user[0]}")

    # query = "SELECT * FROM detail_cart WHERE id_cart = %s"
    # cursor.execute(query, (user_cart[0], ))
    # result = cursor.fetchone()
    # if result is None:
    #     raise HTTPException(status_code=404, detail=f"No product found in cart")

    query = ("INSERT INTO transaction (store_id, date, username) VALUES (%s, NOW(), %s)")
    values = (user[4], user[0])
    cursor.execute(query, values)
    conn.commit()

    query = "SELECT LAST_INSERT_ID()"
    cursor.execute(query)
    current_transaction = cursor.fetchone()[0]

    # insert to detail
    detail = await get_info_cart(user)
    detail = detail[:-1]
    total_price = 0
    for item in detail:
        query = ("INSERT INTO detail_transaction (id_transaction, store_id, id_product, quantity) VALUES (%s, %s, %s, %s)")
        values = (current_transaction, user[4], item[2], item[3])
        cursor.execute(query, values)
        conn.commit()

        query = ("SELECT price FROM product WHERE id_product = %s")
        cursor.execute(query, (item[2], ))
        price = cursor.fetchone()
        total_price += item[3] * price[0]
    
    query = ("UPDATE transaction SET total_price = %s WHERE id_transaction = %s")
    values = (total_price, current_transaction)
    cursor.execute(query, values)
    conn.commit()

    # delete cart detail
    await delete_user_cart(user)

    return f"Transaction success"