from pydantic import BaseModel


class BadRequestError(BaseModel):
    message: str = "Server side error"


class UnauthorizedError(BaseModel):
    message: str = "Unauthorized"
