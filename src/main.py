from src.utils.logging import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.user import router as user_router
from src.api.dependencies import templates


app = FastAPI(title="Referral system API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1", "0.0.0.0"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"{exc}\nEndpoint: {request.url}")

    return templates.TemplateResponse(
        "500_response.html", {"request": request}, status_code=500
    )


@app.exception_handler(404)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"{exc}\nEndpoint: {request.url}")
    return templates.TemplateResponse(
        "404_response.html", {"request": request}, status_code=404
    )


app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])
