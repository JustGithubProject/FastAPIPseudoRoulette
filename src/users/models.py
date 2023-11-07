import sqlalchemy as sql

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String, nullable=False)
