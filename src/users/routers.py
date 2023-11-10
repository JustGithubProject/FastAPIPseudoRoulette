from fastapi import (
    APIRouter,
    Request,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_session
from src.users.models import User
from src.users.schemas import UserCreate
router = APIRouter(tags=["Auth"])


@router.get("/api/list/users")
async def get_users(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Query in order to get all users"""
    query = select(User)
    result = await session.execute(query)
    items = result.scalars().all()

    return items


@router.post("/api/create/user")
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """Query in order to create user"""
    user_obj = User(username=user.username)
    session.add(user_obj)
    await session.commit()
    await session.refresh(user_obj)
    return "The User has been created successfully"
