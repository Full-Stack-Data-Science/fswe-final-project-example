from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from fswe_demo.settings import settings


def get_db_connection() -> Engine:
    """Establishes and returns a connection to the PostgreSQL database."""
    return create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password.get_secret_value()}@"
        f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}",
    )
