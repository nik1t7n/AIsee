from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserResponse
from schemas.token import Token

from services.auth import AuthenticationService

from api.dependencies import get_auth_service

router = APIRouter()

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="auth/login/user", scheme_name="user")

CommonAuthService = Annotated[AuthenticationService, Depends(get_auth_service)]


@router.post(
    "/register/user",
    response_model=Token,
    summary="Register a new user",
    description="Register a new user and return a JWT token"
)
async def register(
        user_create: UserCreate,
        auth_service: CommonAuthService
):
    token = await auth_service.register(user_create)
    return token


@router.post(
    "/login/user/",
    response_model=Token,
    summary="Login for users",
    description="Authenticate a user and return a JWT token"
)
async def login(
        user_login: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthenticationService = Depends(get_auth_service)
):
    token = await auth_service.login(user_login)
    return token


@router.get(
    "/current/user",
    response_model=UserResponse,
    summary="Get current user",
    description="Retrieve information about the currently authenticated user"
)
async def get_current_user(
        auth_service: CommonAuthService,
        token: str = Depends(oauth2_scheme_user),
):
    user = await auth_service.get_current_user(token)
    return user

