# from app.api.server import app
#
# from app.services import auth_service
# from databases import Database
# from starlette.status import HTTP_201_CREATED
# from ward import test
#
#
# @test("auth service saves passwords", tags=["integration"])
# async def _(
#     db: Database,
# ) -> None:
#     user_repo = UsersRepository(db)
#     new_user = {
#         "email": "beyonce@knowles.io",
#         "username": "queenbey",
#         "password": "destinyschild",
#     }
#
#     # send post request to create user and ensure it is successful
#     res = await client.post(
#         app.url_path_for("users:register-new-user"), json={"new_user": new_user}
#     )
#     assert res.status_code == HTTP_201_CREATED
#
#     # ensure that the users password is hashed in the db
#     # and that we can verify it using our auth service
#     user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
#     assert user_in_db is not None
#     assert user_in_db.salt is not None and user_in_db.salt != "123"
#     assert user_in_db.password != new_user["password"]
#     assert auth_service.verify_password(
#         password=new_user["password"],
#         salt=user_in_db.salt,
#         hashed_pw=user_in_db.password,
#     )
