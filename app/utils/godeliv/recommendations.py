from app.utils.config import settings
from app.utils.godeliv.method import *

def get_menu():
    url = f"{settings.godeliv_api_url}/get_menu"
    return get_data(url)

def get_recommendation(id_user: int):
    url = f"{settings.godeliv_api_url}/get_recommendation"

    data = {
        "id_user": id_user
    }

    return get_data(url, data)

def get_standard_recommendation(id_user: int):
    url = f"{settings.godeliv_api_url}/get_standard_recommendation"

    data = {
        "id_user": id_user
    }

    return get_data(url, data)