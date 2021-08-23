from app.db.repositories.users import UsersRepository
from app.models.user import UserInDB
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from integration_tests.fixtures import app, client, db
from ward import test, using


@test("user registration endpoint exists")
@using(client=client, app=app)
async def _(app: FastAPI, client: AsyncClient):
    new_user = {
        "email": "test@email.io",
        "username": "test_username",
        "password": "testpassword",
    }
    res = await client.post(
        app.url_path_for("users:register-new-user"), json={"new_user": new_user}
    )
    assert 200 <= res.status_code < 300


@test("user registration endpoint exists")
@using(client=client, app=app, db=db)
async def _(
    app: FastAPI,
    client: AsyncClient,
    db: Database,
):
    user_repo = UsersRepository(db)
    new_user = {
        "email": "shakira@shakira.io",
        "username": "shakirashakira",
        "password": "chantaje",
    }
    # make sure user doesn't exist yet
    user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
    assert user_in_db is None
    # send post request to create user and ensure it is successful
    res = await client.post(
        app.url_path_for("users:register-new-user"), json={"new_user": new_user}
    )
    assert res.status_code == status.HTTP_201_CREATED
    # ensure that the user now exists in the db
    user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
    assert user_in_db is not None
    assert user_in_db.email == new_user["email"]
    assert user_in_db.username == new_user["username"]
    # check that the user returned in the response is equal to the user in the database
    created_user = UserInDB(**res.json(), password="whatever", salt="123").dict(
        exclude={"password", "salt"}
    )
    assert created_user == user_in_db.dict(exclude={"password", "salt"})


for _attr, _value, _status_code in [
    ("email", "shakira@shakira.io", 400),
    ("username", "shakirashakira", 400),
    ("email", "invalid_email@one@two.io", 422),
    ("password", "short", 422),
    ("username", "shakira@#$%^<>", 422),
    ("username", "ab", 422),
]:

    @test("registering new users")
    @using(client=client, app=app)
    async def _(
        app: FastAPI,
        client: AsyncClient,
        attr=_attr,
        value=_value,
        status_code=_status_code,
    ):
        new_user = {
            "email": "nottaken@email.io",
            "username": "not_taken_username",
            "password": "freepassword",
            attr: value,
        }
        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )
        assert res.status_code == status_code
