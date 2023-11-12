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
from src.users.schemas import UserCreate, UserLogin
from src.users.services import UserRepository
from src.users.utils import create_access_token
from src.users.utils import create_refresh_token
from src.users.utils import verify_password


router = APIRouter(tags=["Auth"])


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)


@router.get("/api/list/users")
async def get_users(user_repository: UserRepository = Depends(get_user_repository)):
    """Query in order to get all users"""
    return await user_repository.get_list_of_users()


@router.post("/api/create/user", summary="Create new user")
async def create_user(user_data: UserCreate, user_repository: UserRepository = Depends(get_user_repository)):
    """Query in order to create user"""
    existing_user = await user_repository.find_user_by_username_(user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return await user_repository.create_user_(user_data)


@router.post("/api/login/user")
async def login(user_data: UserLogin, user_repository: UserRepository = Depends(get_user_repository)):
    existing_user = await user_repository.find_user_by_username_(user_data.username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    hashed_password = existing_user.hashed_password
    if not verify_password(user_data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {
        "access_token": create_access_token(existing_user.username),
        "refresh_token": create_refresh_token(existing_user.username),
    }
