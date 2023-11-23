import sqlalchemy as sql

from src.database import Base


class User(Base):
    """
    User class representing the 'users' table in the database.
    """
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String, nullable=False)
    hashed_password = sql.Column(sql.String, nullable=False)
