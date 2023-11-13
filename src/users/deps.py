from datetime import datetime
import asyncio
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
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
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        print(payload)
        print(token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repository.find_user_by_username_("Kropi")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserGet(**user)


async def main():
    result = await get_current_user(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk4NjAyNjIsInN1YiI6Iktyb3BpIn0.gizhzLPlDOFfTmYd5Lbh5pJXb_awtatVA4QIWdMG0io")
    print(result)

asyncio.run(main())