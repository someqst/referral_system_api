from fastapi import Depends
from src.database.db import get_db
from src.services.user import UserService
from src.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.core.config import BASE_PATH

templates = Jinja2Templates(directory=BASE_PATH / "src/static")


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(session))
