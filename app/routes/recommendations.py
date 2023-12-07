from fastapi import APIRouter, HTTPException
from app.models.product import Product
from typing import Optional
from app.database.database import cursor, conn
from app.utils.auth import user_dependency
from app.utils.godeliv.userData import *
from app.utils.godeliv.recommendations import *
import json

rec_router = APIRouter(
    tags = ["Recommendations"]
)

@rec_router.get('/recommendations/{user_name}')
async def get_recommendation_godeliv(user_name: str):
    data = get_user()
    id_user = 0
    for item in data:
        if user_name == item["nama_user"]:
            id_user = item["id_user"]
            break

    if id_user == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return get_recommendation(id_user)

@rec_router.get('/recommendations')
async def get_standard_recommendation_godeliv(user_name: Optional[str] = None):
    if user_name is None:
        return get_menu()
    
    data = get_user()
    id_user = 0
    for item in data:
        if user_name == item["nama_user"]:
            id_user = item["id_user"]
            break

    if id_user == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return get_standard_recommendation(id_user)

@rec_router.get('/menus/{menu}')
async def get_recipe(menu: str):
    query = "SELECT ingredients FROM menus WHERE menu = %s"
    cursor.execute(query, (menu, ))
    result = cursor.fetchone()
    if result:
        ingredients = json.loads(result[0])
        return ingredients
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have the information at the moment")

@rec_router.get('/menu_information')
async def get_menu_information(ingredient: str):
    query = "SELECT name, brand, aisle FROM product WHERE name LIKE CONCAT ('%', %s, '%')"
    cursor.execute(query, (ingredient, ))
    result = cursor.fetchall()
    if result:
        response = f"{ingredient} is in aisle {result[0][2]}"

        for item in result:
            response += f"- {item[0]} is available with brand {item[1]}\n"
        
        return response
    else:
        raise HTTPException(status_code=404, detail=f"No information found for product {ingredient}")

@rec_router.post('/recommendations')
async def add_user_godeliv(user_name: str, jenis_kelamin: str, umur: int, target_kalori: int):
    return add_user_data(user_name, jenis_kelamin, umur, target_kalori)

