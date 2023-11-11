from fastapi import (
    APIRouter,
    Request,
    Depends
)
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_async_session
from src.users.models import User
from src.users.schemas import UserCreate
from src.users.services import UserRepository


router = APIRouter(tags=["Auth"])


@router.get("/api/list/users")
async def get_users(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Query in order to get all users"""
    query = select(User)
    result = await session.execute(query)
    items = result.scalars().all()

    return items


@router.post("/api/create/user")
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """Query in order to create user"""
    user_repository = UserRepository(session)
    return await user_repository.create_user_(user_data)