from pydantic_settings import BaseSettings


class Environment:
    env_file = ".env"
    env_file_encoding = "utf-8"


class LoadMachineAndDeepLearningModels:
    dl_model: str
    lgbm_lm_model: str
    knn_lm_model: str
    lda_lm_model: str
    ridge_lm_model: str
    sgd_lm_model: str

    gaussian_lpl_model: str
    knn_lpl_model: str
    lgbm_lpl_model: str
    qda_lpl_model: str
    sgd_lpl_model: str

    knn_lc_model: str
    lda_lc_model: str
    lgbm_lc_model: str
    ir_lc_model: str
    ridge_lc_model: str
    

class RabbitMQSettings(BaseSettings):
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_queue: str
    rabbit_exchange: str
    rabbit_routing_key: str 

class DBSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config(Environment):
        pass


class Settings(
    RabbitMQSettings,
    DBSettings,
    LoadMachineAndDeepLearningModels,
):
    pass


settings = Settings()
