from pydantic import BaseModel

class User(BaseModel):
    username: str       # unique name for each user
    password: str       # user password
    name: str           # user name
    role: str           # user role

    class Config:
        json_schema_extra = {
            "example": {
                "username" : "nutrisasi",
                "password" : "rania",
                "name" : "sasi",
                "role" : "admin"
            }
        }