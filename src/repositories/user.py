from typing import List
from src.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self, email: str, hashed_password: str, referrer: int
    ) -> User:
        new_user = User(email=email, password=hashed_password, referrer=referrer)
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_email(self, email: str) -> User | None:
        return (
            await self.session.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()

    async def get_referrer_by_code(self, code: str) -> User | None:
        return (
            await self.session.execute(select(User).where(User.code == code))
        ).scalar_one_or_none()

    async def create_referral_code(
        self, email: str, code: str, code_expiration
    ) -> User:
        stmt = (
            update(User)
            .where(User.email == email)
            .values(code=code, code_expiration=code_expiration)
            .returning(User.email, User.code)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.first()

    async def get_all_referrer_referrals(self, referrer_id: int) -> List[User]:
        stmt = select(User).where(User.referrer == referrer_id)
        return (await self.session.execute(stmt)).scalars().all()
