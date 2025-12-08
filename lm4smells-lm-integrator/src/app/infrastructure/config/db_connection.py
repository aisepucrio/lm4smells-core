from infrastructure.config.settings import settings
import psycopg
from psycopg_pool import ConnectionPool

class DatabaseConnection:
    def __init__(self):
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.database = settings.POSTGRES_DB
        self.dns = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.pool = ConnectionPool(
            conninfo=self.dns,
            min_size=1,
            max_size=5,
            timeout=10
        )
        
    def get_connection(self):
        return self.pool.connection()