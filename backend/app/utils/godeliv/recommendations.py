from app.utils.config import settings
from app.utils.godeliv.method import *

def get_menu():
    url = f"{settings.godeliv_api_url}/get_menu"
    result = get_data(url)
    response = "Here's a few menu you can try\n"
    for item in result:
        name = item["nama_menu"]
        kalori = item["kalori"]
        response += f"{name} has {kalori} calories\n"
    return response

def get_recommendation(id_user: int):
    url = f"{settings.godeliv_api_url}/get_recommendation"

    data = {
        "id_user": id_user
    }

    result = get_data(url, data)
    if result["recommended_meals"] == []:
        return "Unfortunately, we don't have menus lower than your target calories"
    else:
        meals = result["recommended_meals"]
        response = "Here's a few menu you can try based on your target calories\n"
        for item in meals:
            name = item["nama_menu"]
            kalori = item["kalori"]
            response += f"{name} has {kalori} calories\n"
        return response

def get_standard_recommendation(id_user: int):
    url = f"{settings.godeliv_api_url}/get_standard_recommendation"

    data = {
        "id_user": id_user
    }

    result = get_data(url, data)
    if result["recommended_meals"] == []:
        return "Unfortunately, we don't have menus suited to your age and gender"
    else:
        meals = result["recommended_meals"]
        response = "Here's a few menu you can try based on your age and gender\n"
        response += "Gotta watch out for those calories, right? :D\n"
        for item in meals:
            name = item["nama_menu"]
            kalori = item["kalori"]
            response += f"{name} has {kalori} calories\n"
        return response