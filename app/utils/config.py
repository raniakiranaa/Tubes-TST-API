from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str

    # Godeliv API
    godeliv_api_url: str
    godeliv_api_username: str
    godeliv_api_password: str

    class Config:
        env_file = '.env'

settings = Settings()

