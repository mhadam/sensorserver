from typing import Union, Optional

import jwt
from app.api.dependencies.auth import fastapi_users
from app.core.config import (
    SECRET_KEY,
    JWT_AUDIENCE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
)
from app.models.user import User
from app.services.authentication import (
    create_access_token_for_user,
)
from databases import Database
from fastapi import FastAPI, HTTPException
from fastapi_users.user import UserNotExists
from httpx import AsyncClient
from integration_tests.fixtures import app, client, db, user, authorized_client
from pydantic import ValidationError
from starlette import status
from starlette.datastructures import Secret
from ward import test, using, raises


@test("user registration endpoint exists")
@using(client=client, app=app)
async def _(app: FastAPI, client: AsyncClient):
    new_user = {
        "email": "test@email.io",
        "password": "testpassword",
    }
    res = await client.post("/api/auth/register", json=new_user)
    assert 200 <= res.status_code < 300


@test("users can be created")
@using(client=client, app=app)
async def _(
    app: FastAPI,
    client: AsyncClient,
):
    new_user = {
        "email": "shakira@shakira.io",
        "password": "chantaje",
    }
    # make sure user doesn't exist yet
    rows = await app.state._db.fetch_all(query="\dt")
    print([row for row in rows])
    breakpoint()
    with raises(UserNotExists):
        await fastapi_users.get_user(new_user["email"])
    # send post request to create user and ensure it is successful
    res = await client.post(
        app.url_path_for("users:register-new-user"), json={"new_user": new_user}
    )
    assert res.status_code == status.HTTP_201_CREATED
    # ensure that the user now exists in the db
    user_in_db = await fastapi_users.get_user(new_user["email"])
    assert user_in_db is not None
    assert user_in_db.email == new_user["email"]
    assert user_in_db.username == new_user["username"]
    # check that the user returned in the response is equal to the user in the database
    created_user = User(**res.json()).dict(exclude={"access_token"})
    assert created_user == user_in_db.dict(exclude={"password", "salt"})


#
#
# for _attr, _value, _status_code in [
#     ("email", "shakira@shakira.io", 400),
#     ("username", "shakirashakira", 400),
#     ("email", "invalid_email@one@two.io", 422),
#     ("password", "short", 422),
#     ("username", "shakira@#$%^<>", 422),
#     ("username", "ab", 422),
# ]:
#
#     @test("registering new users")
#     @using(client=client, app=app)
#     async def _(
#         app: FastAPI,
#         client: AsyncClient,
#         attr=_attr,
#         value=_value,
#         status_code=_status_code,
#     ):
#         new_user = {
#             "email": "nottaken@email.io",
#             "username": "not_taken_username",
#             "password": "freepassword",
#             attr: value,
#         }
#         res = await client.post(
#             app.url_path_for("users:register-new-user"), json={"new_user": new_user}
#         )
#         assert res.status_code == status_code
#
#
# @test("passwords are hashed and salted")
# @using(client=client, app=app, db=db)
# async def _(app: FastAPI, client: AsyncClient, db: Database):
#     user_repo = UsersRepository(db)
#     new_user = {
#         "email": "beyonce@knowles.io",
#         "username": "queenbey",
#         "password": "destinyschild",
#     }
#     # send post request to create user and ensure it is successful
#     res = await client.post(
#         app.url_path_for("users:register-new-user"), json={"new_user": new_user}
#     )
#     assert res.status_code == status.HTTP_201_CREATED
#     # ensure that the users password is hashed in the db
#     # and that we can verify it using our auth service
#     user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
#     assert user_in_db is not None
#     assert user_in_db.salt is not None and user_in_db.salt != "123"
#     assert user_in_db.password != new_user["password"]
#     assert verify_password(
#         password=new_user["password"],
#         salt=user_in_db.salt,
#         hashed_pw=user_in_db.password,
#     )
#
#
# @test("can create access token successfully")
# @using(client=client, app=app, test_user=user)
# async def _(app: FastAPI, client: AsyncClient, test_user: UserDB):
#     access_token = create_access_token_for_user(
#         user=test_user,
#         secret_key=str(SECRET_KEY),
#         audience=JWT_AUDIENCE,
#         expires_in=ACCESS_TOKEN_EXPIRE_MINUTES,
#     )
#
#     creds = jwt.decode(
#         access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
#     )
#     assert creds.get("username") is not None
#     assert creds["username"] == test_user.username
#     assert creds["aud"] == JWT_AUDIENCE
#
#
# @test("token missing user is invalid")
# @using(client=client, app=app)
# async def _(app: FastAPI, client: AsyncClient):
#     access_token = create_access_token_for_user(
#         user=None,
#         secret_key=str(SECRET_KEY),
#         audience=JWT_AUDIENCE,
#         expires_in=ACCESS_TOKEN_EXPIRE_MINUTES,
#     )
#
#     with raises(jwt.PyJWTError):
#         jwt.decode(
#             access_token,
#             str(SECRET_KEY),
#             audience=JWT_AUDIENCE,
#             algorithms=[JWT_ALGORITHM],
#         )
#
#
# for _secret_key, _jwt_audience, _exception in [
#     ("wrong-secret", JWT_AUDIENCE, jwt.InvalidSignatureError),
#     (None, JWT_AUDIENCE, jwt.InvalidSignatureError),
#     (SECRET_KEY, "othersite:auth", jwt.InvalidAudienceError),
#     (SECRET_KEY, None, ValidationError),
# ]:
#
#     @test("invalid token content raises error")
#     @using(client=client, app=app, test_user=user)
#     async def _(
#         app: FastAPI,
#         client: AsyncClient,
#         test_user: UserDB,
#         secret_key: Union[str, Secret] = _secret_key,
#         jwt_audience: str = _jwt_audience,
#         exception=_exception,
#     ):
#         with raises(exception):
#             access_token = create_access_token_for_user(
#                 user=test_user,
#                 secret_key=str(secret_key),
#                 audience=jwt_audience,
#                 expires_in=ACCESS_TOKEN_EXPIRE_MINUTES,
#             )
#
#             jwt.decode(
#                 access_token,
#                 str(SECRET_KEY),
#                 audience=JWT_AUDIENCE,
#                 algorithms=[JWT_ALGORITHM],
#             )
#
#
# @test("user can login successfully and receives valid token")
# @using(client=client, app=app, test_user=user)
# async def _(
#     app: FastAPI,
#     client: AsyncClient,
#     test_user: UserDB,
# ):
#     client.headers["content-type"] = "application/x-www-form-urlencoded"
#     login_data = {
#         "username": test_user.email,
#         "password": "heatcavslakers",  # insert user's plaintext password
#     }
#     res = await client.post(
#         app.url_path_for("users:login-email-and-password"), data=login_data
#     )
#     assert res.status_code == status.HTTP_200_OK
#     # check that token exists in response and has user encoded within it
#     token = res.json().get("access_token")
#     creds = jwt.decode(
#         token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
#     )
#     assert "username" in creds
#     assert creds["username"] == test_user.username
#     assert "sub" in creds
#     assert creds["sub"] == test_user.email
#     # check that token is proper type
#     assert "token_type" in res.json()
#     assert res.json().get("token_type") == "bearer"
#
#
# for _credential, _wrong_value, _status_code in [
#     ("email", "wrong@email.com", 401),
#     ("email", None, 422),
#     ("email", "notemail", 401),
#     ("password", "wrongpassword", 401),
#     ("password", None, 422),
# ]:
#
#     @test("user with wrong credentials doesn't receive token")
#     @using(client=client, app=app, test_user=user)
#     async def _(
#         app: FastAPI,
#         client: AsyncClient,
#         test_user: UserDB,
#         credential: str = _credential,
#         wrong_value: str = _wrong_value,
#         status_code: int = _status_code,
#     ):
#         client.headers["content-type"] = "application/x-www-form-urlencoded"
#         user_data = test_user.dict()
#         user_data["password"] = "heatcavslakers"  # insert user's plaintext password
#         user_data[credential] = wrong_value
#         login_data = {
#             "username": user_data["email"],
#             "password": user_data["password"],  # insert password from parameters
#         }
#         res = await client.post(
#             app.url_path_for("users:login-email-and-password"), data=login_data
#         )
#         assert res.status_code == status_code
#         assert "access_token" not in res.json()
#
#
# @test("retrieves username from token")
# @using(client=client, app=app, test_user=user)
# async def _(app: FastAPI, client: AsyncClient, test_user: UserDB):
#     token = create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
#     username = get_username_from_token(token=token, secret_key=str(SECRET_KEY))
#     assert username == test_user.username
#
#
# for _secret, _wrong_token in [
#     (SECRET_KEY, "asdf"),  # use wrong token
#     (SECRET_KEY, ""),  # use wrong token
#     (SECRET_KEY, None),  # use wrong token
#     ("ABC123", "use correct token"),  # use wrong secret
# ]:
#
#     @test("error when token or secret is wrong")
#     @using(client=client, app=app, test_user=user)
#     async def _(
#         app: FastAPI,
#         client: AsyncClient,
#         test_user: UserDB,
#         secret: Union[Secret, str] = _secret,
#         wrong_token: Optional[str] = _wrong_token,
#     ):
#         token = create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
#         if wrong_token == "use correct token":
#             wrong_token = token
#         with raises(HTTPException):
#             get_username_from_token(token=wrong_token, secret_key=str(secret))
#
#
# @test("authenticated user can retrieve own data")
# @using(client=authorized_client, app=app, test_user=user)
# async def _(
#     app: FastAPI,
#     client: AsyncClient,
#     test_user: UserDB,
# ):
#     res = await client.get(app.url_path_for("users:get-current-user"))
#     assert res.status_code == status.HTTP_200_OK
#     user = UserPublic(**res.json())
#     assert user.email == test_user.email
#     assert user.username == test_user.username
#     assert user.id == test_user.id
#
#
# @test("user cannot access own data if not authenticated")
# @using(client=client, app=app, test_user=user)
# async def _(
#     app: FastAPI,
#     client: AsyncClient,
#     test_user: UserDB,
# ):
#     res = await client.get(app.url_path_for("users:get-current-user"))
#     assert res.status_code == status.HTTP_401_UNAUTHORIZED
#
#
# for _jwt_prefix in ["", "value", "Token", "JWT", "Swearer"]:
#
#     @test("user cannot access own data with incorrect jwt prefix")
#     @using(client=client, app=app, test_user=user)
#     async def test_user_cannot_access_own_data_with_incorrect_jwt_prefix(
#         app: FastAPI,
#         client: AsyncClient,
#         test_user: UserDB,
#         jwt_prefix: str = _jwt_prefix,
#     ):
#         token = create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
#         res = await client.get(
#             app.url_path_for("users:get-current-user"),
#             headers={"Authorization": f"{jwt_prefix} {token}"},
#         )
#         assert res.status_code == status.HTTP_401_UNAUTHORIZED
