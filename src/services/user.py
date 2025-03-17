from src.utils.auth import get_password_hash
from src.repositories.user import UserRepository
from datetime import datetime, timezone, timedelta
from src.schemas.user import (
    UserCreate,
    UserResponse,
    UsersResponse,
    CreatedCodeResponse,
)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate, code: str | None):
        hashed_password = get_password_hash(user_data.password)
        referrer_id = None
        if code:
            referrer = await self.get_referrer_by_code_if_not_expired(code)
            if referrer:
                referrer_id = referrer.id

        user = await self.user_repo.create_user(
            email=user_data.email, hashed_password=hashed_password, referrer=referrer_id
        )
        return UserResponse.model_validate(user)

    async def get_referrer_by_code_if_not_expired(self, code: str):
        user = await self.user_repo.get_referrer_by_code(code)
        if not user:
            return None

        if user.code_expiration < datetime.now().replace(tzinfo=None):
            return None
        return user

    async def get_user_by_email(self, email: str):
        user = await self.user_repo.get_user_by_email(email)
        return user

    async def create_code(self, email: str, code: str):
        expire = (datetime.now(timezone.utc) + timedelta(days=30)).replace(tzinfo=None)
        user = await self.user_repo.create_referral_code(email, code, expire)
        return CreatedCodeResponse.model_validate(user)

    async def get_all_referrer_referrals(self, referrer_id: int):
        referrals = await self.user_repo.get_all_referrer_referrals(referrer_id)
        return UsersResponse.model_validate(
            {"users": [UserResponse.model_validate(referral) for referral in referrals]}
        )
