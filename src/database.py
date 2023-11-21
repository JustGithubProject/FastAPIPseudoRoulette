from typing import AsyncGenerator

from sqlalchemy import Table
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from src.config import (
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DB_NAME
)

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'


Base = declarative_base()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def clear_table_and_reset_autoincrement(table_name):
    async with async_session_maker() as session:
        # Удаляем данные из таблицы
        table = Table(table_name, Base.metadata, autoload_with=engine)
        delete_stmt = table.delete()
        await session.execute(delete_stmt)

        # Сбрасываем счетчик автоинкремента
        sequence_name = f"{table_name}_id_seq"
        reset_sequence_sql = text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
        await session.execute(reset_sequence_sql)


