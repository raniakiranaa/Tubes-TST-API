from fastapi import APIRouter, HTTPException
from app.models.user import User
from typing import Optional
from app.database.database import cursor, conn
from app.utils.auth import hash_password
from app.utils.auth import user_dependency
from app.utils.godeliv.userData import *
from starlette import status

user_router = APIRouter(
    tags = ["User"]
)

@user_router.get('/user')
async def retrieve_all_users(user: user_dependency):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    # get users from admin's store
    query = ("SELECT * FROM user WHERE store_id = %s")
    cursor.execute(query, (user[4], ))
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No user found")

@user_router.post("/user")
async def create_user(username: str, password: str, name: str, store_id: str):
    # validate input
    if not username or not password or not name:
        raise HTTPException(status_code=422, detail=f"Username, password, and name are required fields. New user has not been added")
    
    query = ("SELECT * FROM user")
    cursor.execute(query)
    users = cursor.fetchall()
    for item in users:
        if username == item[0]:
            raise HTTPException(status_code=422, detail=f"Username is taken. Choose another username")
    
    if len(username) > 25 or len(password) > 25 or len(name) > 25:
        raise HTTPException(status_code=422, detail="Data exceeds the length limit. Fill out a shorter data")
    
    hashed_password = hash_password(password)
    query = ("INSERT INTO user VALUES (%s, %s, %s, %s, %s)")
    # assign all new users as a customer
    values = (username, hashed_password, name, 'customer', store_id)
    cursor.execute(query, values)
    conn.commit()
    return f"User {username} has been added"

@user_router.put('/user/{username}', response_model= str)
async def update_user(user: user_dependency, username: str, password: Optional[str] = None, name: Optional[str] = None, role: Optional[str] = None):
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username, ))
    result = cursor.fetchone()

    # validate role (has to be admin from the same store)
    if user[3] != 'admin' or user[4] != result[4]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")
    
    if result:
        query = "UPDATE user SET"
        values = []
        if password is not None:
            hashed_password = hash_password(user.password)
            query += " password = %s,"
            values.append(hashed_password)
        if name is not None:
            query += " name = %s,"
            values.append(name)
        if role is not None:
            if role in ('admin', 'customer'):
                query += " role = %s,"
                values.append(role)
            else:
                raise HTTPException(status_code=422, detail=f"Role is not valid. Role can only be between admin or customer")
        if not (password or name or role):
            raise HTTPException(status_code=422, detail=f"No new input data")
        
        # remove trailing comma
        query = query.rstrip(',') + " WHERE username = %s"
        values.append(username)

        cursor.execute(query, tuple(values))
        conn.commit()

        return f"User {username} has been updated"
    
    else:
        raise HTTPException(status_code=404, detail=f"No user found with username {username}")

@user_router.delete('/user/{username}', response_model=str)
async def delete_user(user: user_dependency, username: str):
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username, ))
    result = cursor.fetchone()

    # validate role (has to be admin from the same store)
    if user[3] != 'admin' or user[4] != result[4]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    if result:
        query = "DELETE FROM user WHERE username = %s"
        cursor.execute(query, (username, ))
        conn.commit()
        return f"User with username {username} has been deleted"
    else:
        raise HTTPException(status_code=404, detail=f"No user found with username {username}")