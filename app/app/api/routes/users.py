from app.api.dependencies.auth import fastapi_users
from app.core.auth import cookie_authentication
from fastapi import APIRouter

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(cookie_authentication, requires_verification=True),
    prefix="/auth/cookie",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

# @router.post(
#     "/",
#     response_model=UserPublic,
#     name="users:register-new-user",
#     status_code=HTTP_201_CREATED,
# )
# async def register_new_user(
#     new_user: UserCreate = Body(...),
#     user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
# ) -> UserPublic:
#     created_user = await user_repo.register_new_user(new_user=new_user)
#     access_token = AccessToken(
#         access_token=create_access_token_for_user(user=created_user),
#         token_type="bearer",
#     )
#     return UserPublic(**created_user.dict(), access_token=access_token)
#
#
# @router.post(
#     "/login/token/", response_model=AccessToken, name="users:login-email-and-password"
# )
# async def user_login_with_email_and_password(
#     user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
#     form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
# ) -> AccessToken:
#     user = await user_repo.authenticate_user(
#         email=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authentication was unsuccessful.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = AccessToken(
#         access_token=create_access_token_for_user(user=user), token_type="bearer"
#     )
#     return access_token
#
#
# @router.get("/me/", response_model=UserPublic, name="users:get-current-user")
# async def get_currently_authenticated_user() -> UserPublic:
#     return None
# @router.get(
#     "/users/me",
#     name="users:authorize",
#     status_code=status.HTTP_200_OK,
# )
# async def authorize_device(
#     device_id: str,
#     request: Request,
#     response: Response,
#     session: AsyncSession = Depends(get_session),
# ):
#     pass
