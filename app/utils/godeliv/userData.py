from app.utils.config import settings
from app.utils.godeliv.method import *

def get_user():
    url = f"{settings.godeliv_api_url}/get_user"
    return get_data(url)

def get_last_id_user():
    users = get_user()
    if users:
        last_user_id = max(users, key=lambda user: user["id_user"])["id_user"]
        return last_user_id
    else:
        return 0
    
def add_user_data(user_name: str, jenis_kelamin: str, umur: int, target_kalori: int):
    last_id = get_last_id_user()
    url = f"{settings.godeliv_api_url}/add_user"

    data = {
        "id_user": last_id + 1,
        "nama_user" : user_name,
        "jenis_kelamin" : jenis_kelamin,
        "umur_user" : umur,
        "target_kalori" : target_kalori
    }

    return post_data(url, data)