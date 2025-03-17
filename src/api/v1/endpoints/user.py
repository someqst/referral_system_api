from src.utils.logging import logger
from src.utils.auth import check_token
from src.services.user import UserService
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi import APIRouter, Depends, status
from src.api.dependencies import get_user_service, templates
from src.schemas.user import UsersResponse, CreatedCodeResponse
from src.schemas.errors import BadRequestError, UnauthorizedError


router = APIRouter()


# Тут как и было сказано, что код хранится где-то на фронте, а потом JSом забирается оттуда. Но эт над нормальный фронт писать - не хочетса
@router.get(
    "/enter/{referral_code}",
    summary="Переход в регистрацию с реферальным кодом",
    responses={
        status.HTTP_200_OK: {
            "content": "text/html",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": "text/html",
        },
    },
    response_class=HTMLResponse,
)
async def set_referal_code(
    request: Request,
    referral_code: str,
    user_service: UserService = Depends(get_user_service),
):
    referrer = await user_service.get_referrer_by_code_if_not_expired(referral_code)
    if referrer:

        response = templates.TemplateResponse(
            "200_response.html",
            {"request": request, "referral_code": referral_code},
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie("code", referral_code, secure=True, httponly=True)
        logger.info(f"Перешел пользователь по реферальному коду {referral_code}")
        return response

    return templates.TemplateResponse(
        "404_response.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND
    )


@router.post(
    "/create_code",
    summary="Создание реферального кода",
    responses={
        status.HTTP_201_CREATED: {"model": CreatedCodeResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)
async def create_code(
    code: str,
    token: dict = Depends(check_token),
    user_service: UserService = Depends(get_user_service),
):
    email = token.get("email")
    return await user_service.create_code(email, code)


@router.get(
    "/get_referrals/{referrer_id}",
    response_model=UsersResponse,
    summary="Получение всех реферралов по id реферрера",
)
async def get_all_referrer_referrals(
    referrer_id: int, user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_referrer_referrals(referrer_id)
