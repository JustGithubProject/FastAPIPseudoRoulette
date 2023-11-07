from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base


from src.config import Config


SQLALCHEMY_DATABASE_URL = f'mysql://{Config.USERNAME}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.DB_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

