from fastapi import (
    APIRouter,
    Request,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
router = APIRouter(tags=["Auth"])


@router.get("/api/list/users")
async def get_users(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Query in order to get all users"""
    ...