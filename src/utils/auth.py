from jose import jwt
from fastapi import status, Request, Response
from src.core.config import get_auth_data
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(jwt_token):
    auth_data = get_auth_data()
    decode_jwt = jwt.decode(jwt_token, auth_data["secret_key"], auth_data["algorithm"])
    return decode_jwt


async def check_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        return jwt.decode(
            token, get_auth_data()["secret_key"], get_auth_data()["algorithm"]
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )


async def authenticate_user(
    password: str, hashed_password: str, email: str
):
    if not verify_password(plain_password=password, hashed_password=hashed_password):
        return None
    encoded_jwt = create_access_token({"email": email})
    return encoded_jwt
