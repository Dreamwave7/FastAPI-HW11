from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sql_key :str
    algm:str
    secret:str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()