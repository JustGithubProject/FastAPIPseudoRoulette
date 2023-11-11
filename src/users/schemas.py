from pydantic import BaseModel


class UserGet(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str
    password: str

