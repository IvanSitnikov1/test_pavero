from fastapi import FastAPI

from auth.base_config import auth_backend
from auth.schemas import UserRead, UserCreate
from files.router import router as router_files
from auth.base_config import fastapi_users

app = FastAPI(
    title="Test_Pavero"
)

# роутер для регистрации пользователя
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# роутер для авторизации пользователя
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# роутер для загрузки и чтения файлов
app.include_router(router_files)
