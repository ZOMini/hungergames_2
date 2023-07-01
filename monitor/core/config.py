from pydantic import BaseModel
from pydantic_settings_yaml import YamlBaseSettings


class Database(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: int
    url_async: str = ''
    url_sync: str = ''


class Redis(BaseModel):
    host: str
    port: int
    url: str = ''

class Logger(BaseModel):
    count: int
    file: str
    encoding: str

class Jwt(BaseModel):
    disabled_in_api: bool
    secret_key: str
    access_token_expires: int

class Worker(BaseModel):
    http_timeout: int
    interval: int
    time_of_unavailability: int

class App(BaseModel):
    debug: bool
    migrate: bool
    flask_secret_key: str
    salt_password: str
    logger: Logger
    jwt: Jwt
    worker: Worker

class Settings(YamlBaseSettings):
    app: App
    db: Database
    redis: Redis

    class Config:
        yaml_file = "./env.yaml"


settings = Settings()
settings.db.url_async = f'postgresql+asyncpg://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}'
settings.db.url_sync = f'postgresql://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}'
settings.redis.url = f'redis://{settings.redis.host}:{settings.redis.port}'
