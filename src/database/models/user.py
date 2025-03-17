from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(254), unique=True)
    code: Mapped[str | None]
    code_expiration: Mapped[datetime | None]
    referrer: Mapped[int | None] = mapped_column(ForeignKey(id))
