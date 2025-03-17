from src.utils.logging import logger
from src.services.user import UserService
from fastapi.responses import JSONResponse
from src.utils.auth import authenticate_user
from src.api.dependencies import get_user_service
from src.schemas.user import UserResponse, UserCreate
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status


router = APIRouter()


@router.post(
        "/register",
        responses={
            status.HTTP_201_CREATED: {"model": UserResponse},
            status.HTTP_409_CONFLICT: {"detail": "Email already in use"}
            },
        response_model=UserResponse
)
async def register_user(
    request: Request,
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
        )

    logger.info(f"Зарегистрирован пользователь: {user_data.email}")
    return await user_service.create_user(user_data, request.cookies.get("code"))


@router.post(
        "/login",
        responses={
            status.HTTP_401_UNAUTHORIZED: {"detail": "User successfully logged in!"},
            status.HTTP_200_OK: {"message": "User successfully loggined in!"}
        },
        response_model=dict
)
async def login_user(
    response: Response,
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password"
        )

    token = await authenticate_user(
        user_data.password, user.password, user_data.email
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password"
        )

    logger.info(f"Вошел пользователь: {user_data.email}")

    response.set_cookie("user_access_token", token)
    response = JSONResponse(
        content={"detail": "User successfully logged in!"},
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie("user_access_token", token, secure=True, httponly=True)
    return response


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response = JSONResponse(
        content={"message": "User logged out successfully"},
        status_code=status.HTTP_200_OK,
    )
    response.delete_cookie(key="user_access_token", secure=True, httponly=True)
    return response
