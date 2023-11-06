from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

SQLALCHEMY_DATABASE_URL = f"postgresql://{Config.USERNAME}:{Config.PASSWORD}@{Config.HOST}/{Config.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

