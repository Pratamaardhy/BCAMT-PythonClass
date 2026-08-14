from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.controllers import auth_controller, bank_account_controller
from app.core.config import get_settings
from app.core.exceptions import AppError

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}
    )


app.include_router(auth_controller.router, prefix=settings.API_V1_PREFIX)
app.include_router(
    bank_account_controller.router, prefix=settings.API_V1_PREFIX
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
