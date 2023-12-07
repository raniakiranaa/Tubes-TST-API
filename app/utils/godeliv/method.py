import requests
import json
from app.utils.config import settings

def get_access_token():
    url = f"{settings.godeliv_api_url}/token"
    data = {
        "username": settings.godeliv_api_username,
        "password": settings.godeliv_api_password
    }

    response = requests.post(url, data=data)
    return response.json()['access_token']

def get_data(url : str, data : dict = None):
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    if data:
        response = requests.get(url, headers=headers, params=data)
    else:
        response = requests.get(url, headers=headers)
    
    return response.json()

def post_data(url : str, data : dict):
    headers = {
        'Authorization' : f'Bearer {get_access_token()}'
    }

    response = requests.post(url, headers=headers, params=data)
    return response.json()

def put_data(url : str):
    headers = {
        'Authorization' : f'Bearer {get_access_token()}'
    }
    response = requests.put(url, headers=headers)
    return response.json()

def delete_data(url : str):
    headers = {
        'Authorization' : f'Bearer {get_access_token()}'
    }
    response = requests.delete(url, headers=headers)
    return response.json()