from pydantic_settings import BaseSettings


class Environment:
    env_file = ".env"
    env_file_encoding = "utf-8"


class RabbitMQSettings(BaseSettings):
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_queue: str
    rabbit_exchange: str
    rabbit_routing_key: str 

    
    class Config(Environment):
        pass


class Settings(
    RabbitMQSettings,
):
    pass


settings = Settings()
