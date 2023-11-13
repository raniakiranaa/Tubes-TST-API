from fastapi import APIRouter, HTTPException
from ..models.user import User
from typing import Optional
from ..database.database import cursor, conn
from ..services.auth import hash_password
from ..services.auth import user_dependency
from starlette import status

user_router = APIRouter(
    tags = ["User"]
)

@user_router.get('/user')
async def retrieve_all_users(user: user_dependency):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = ("SELECT * FROM user")
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No user found")

@user_router.post("/user", response_model=str)
async def create_user(user: User, current_user: user_dependency):
    # validate role
    if current_user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    # validate input
    if not user.username:
        raise HTTPException(status_code=422, detail=f"Username is a required field. New user has not been added")
    
    users = await retrieve_all_users(current_user)
    for item in users:
        if user.username == item[0]:
            raise HTTPException(status_code=422, detail=f"Username is taken. Choose another username")
    
    if len(user.username) > 25 or len(user.username) > 25 or len(user.name) > 25:
        raise HTTPException(status_code=422, detail="Data exceeds the length limit. Fill out a shorter data")
    if user.role != 'admin' and user.role != 'customer':
        raise HTTPException(status_code=422, detail=f"Role is not valid. Role can only be between admin or customer")
    
    hashed_password = hash_password(user.password)
    query = ("INSERT INTO user VALUES (%s, %s, %s, %s)")
    values = (user.username, hashed_password, user.name, user.role)
    cursor.execute(query, values)
    conn.commit()
    return f"User {user.username} has been added"

@user_router.put('/user/{username}', response_model= str)
async def update_user(user: user_dependency, username: str, password: Optional[str] = None, name: Optional[str] = None, role: Optional[str] = None):
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username, ))
    result = cursor.fetchone()
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
    # validate role
    if user[3] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username, ))
    result = cursor.fetchone()
    if result:
        query = "DELETE FROM user WHERE username = %s"
        cursor.execute(query, (username, ))
        conn.commit()
        return f"User with username {username} has been deleted"
    else:
        raise HTTPException(status_code=404, detail=f"No user found with username {username}")