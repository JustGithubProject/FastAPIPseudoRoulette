from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users.models import User
from src.users.schemas import UserCreate
from src.users.utils import get_hashed_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list_of_users(self):
        query = select(User)
        result = await self.session.execute(query)
        items = result.scalars().all()
        return items

    async def find_user_by_username_(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar()
        return user

    async def create_user_(self, user_data: UserCreate) -> User:
        user_obj = User(username=user_data.username, hashed_password=get_hashed_password(user_data.password))
        self.session.add(user_obj)
        await self.session.commit()
        await self.session.refresh(user_obj)
        return user_obj