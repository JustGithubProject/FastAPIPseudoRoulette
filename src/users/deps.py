from datetime import datetime
import asyncio
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import ValidationError

from src.users.services import UserRepository
from src.users.utils import ALGORITHM
from src.users.utils import JWT_SECRET_KEY
from src.users.schemas import TokenPayload
from src.users.schemas import UserGet
from src.database import get_async_session

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)


async def get_current_user(token: str = Depends(reuseable_oauth),
                           user_repository: UserRepository = Depends(get_user_repository)) -> UserGet:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_repository.find_user_by_username_(username)
    if not user:
        raise credentials_exception

    return user



