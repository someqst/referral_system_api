from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr
from typing import ClassVar, List


class BaseResponseModel(BaseModel):
    model_config: ClassVar[dict] = ConfigDict(from_attributes=True, extra="ignore")


class UserCreate(BaseResponseModel):
    email: EmailStr
    password: str


class UserResponse(BaseResponseModel):
    id: int
    email: EmailStr


class UsersResponse(BaseResponseModel):
    users: List["UserResponse"]


class CreatedCodeResponse(BaseResponseModel):
    email: EmailStr
    code: str
