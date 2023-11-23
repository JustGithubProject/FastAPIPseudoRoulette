from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users.models import User
from src.users.schemas import UserCreate
from src.users.utils import get_hashed_password


class UserRepository:
    """UserRepository class for handling user-related database operations."""
    def __init__(self, session: AsyncSession):
        """
        Initializes a new instance of the UserRepository.
        Args:
            session (AsyncSession): The SQLAlchemy AsyncSession to be used for database operations.
        """
        self.session = session

    async def get_list_of_users(self):
        """Retrieve a list of all users from the database."""
        query = select(User)
        result = await self.session.execute(query)
        items = result.scalars().all()
        return items

    async def find_user_by_username_(self, username: str) -> Optional[User]:
        """
            Find a user in the database by their username.
            Args:
            username (str): The username to search for.
            Returns:
                Optional[User]: The user object if found, otherwise None.
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar()
        return user

    async def create_user_(self, user_data: UserCreate) -> User:
        """
         Create a new user in the database.

         Args:
             user_data (UserCreate): UserCreate data class containing user information.

         Returns:
             User: The newly created user object.
         """
        user_obj = User(username=user_data.username, hashed_password=get_hashed_password(user_data.password))
        self.session.add(user_obj)
        await self.session.commit()
        await self.session.refresh(user_obj)
        return user_obj