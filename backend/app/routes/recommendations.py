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
async def get_recommendation_godeliv(user: user_dependency, user_name: str, target_kalori: int):
    id_user = 0
    add_target_kalori(user_name, target_kalori)
    data = get_user()
    for item in data:
        if user_name == item["nama_user"]:
            id_user = item["id_user"]
    
    return get_recommendation(id_user)

@rec_router.get('/recommendations')
async def get_standard_recommendation_godeliv(user: user_dependency, user_name: Optional[str] = None, umur: Optional[int] = None, jenis_kelamin: Optional[str] = None):
    if user_name is None:
        return get_menu()
    
    add_umur_gender(user_name, umur, jenis_kelamin)
    data = get_user()
    id_user = 0
    for item in data:
        if user_name == item["nama_user"]:
            id_user = item["id_user"]
    
    return get_standard_recommendation(id_user)

@rec_router.get('/menus/{menu}')
async def get_recipe(user: user_dependency, menu: str):
    query = "SELECT ingredients FROM menus WHERE menu = %s"
    cursor.execute(query, (menu, ))
    result = cursor.fetchone()
    if result:
        ingredients = json.loads(result[0])
    
        if ingredients:
            response = f"To prepare a {menu}, you'll need: {', '.join(ingredients[:-1])}"
            if len(ingredients) > 1:
                response += f", and {ingredients[-1]}"
        else:
            response = f"There are no ingredients listed for {menu}."
        
        return response
    else:
        raise HTTPException(status_code=404, detail="Sorry, we don't have the information at the moment")

@rec_router.post('/recommendations')
async def add_user_godeliv(user: user_dependency, user_name: str, jenis_kelamin: str, umur: int, target_kalori: int):
    return add_user_data(user_name, jenis_kelamin, umur, target_kalori)

