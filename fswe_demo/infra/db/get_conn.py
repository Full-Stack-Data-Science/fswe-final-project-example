from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from fswe_demo.settings import settings


def get_db_connection() -> Engine:
    """Establishes and returns a connection to the PostgreSQL database."""
    return create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password.get_secret_value()}@"
        f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}",
    )


engine = get_db_connection()


def get_session() -> Generator[Session]:
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Base(DeclarativeBase):
    pass
