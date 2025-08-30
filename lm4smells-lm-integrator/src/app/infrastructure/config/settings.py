from pydantic_settings import BaseSettings

class Environment:
    env_file = ".env"
    env_file_encoding = "utf-8"

class RabbitMQSettings(BaseSettings):
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_virtual_host: str
    rabbit_queue: str
    rabbit_exchange: str
    rabbit_routing_key: str
    rabbit_batch_size: int

    class Config(Environment):
        pass


class LMSettings(BaseSettings):
    lm_ollama_host: str
    llm_gpt_host: str
    llm_gpt_api_key: str

    class Config(Environment):
        pass


class DBSettings(BaseSettings):
    db_path: str

    class Config(Environment):
        pass


class Settings(
    RabbitMQSettings,
    LMSettings,
    DBSettings,
):
    pass


settings = Settings()
