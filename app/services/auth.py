from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from ..models.token import Token
from ..database.database import cursor
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
# hide
SECRET_KEY = '******************'
ALGORITHM = '*****'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def hash_password(password: str):
    return bcrypt_context.hash(password)

@auth_router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"},)
    
    token = create_access_token(user[0], timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str):
    query = ("SELECT * FROM USER where username = %s")
    cursor.execute(query, (username, ))
    result = cursor.fetchone()
    if result is None:
        return False
    
    if not bcrypt_context.verify(password, result[1]):
        return False
    
    return result

def create_access_token(username: str, expires_delta: timedelta):
    encode = {'sub': username}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please authenticate.')
        
        query = ("SELECT * FROM user WHERE username = %s")
        cursor.execute(query, (username, ))
        result = cursor.fetchone()
        return result
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please authenticate.")
    
user_dependency = Annotated[dict, Depends(get_current_user)]