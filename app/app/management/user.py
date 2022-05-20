import asyncio
from typing import Optional

import typer
from fastapi_users.models import BaseUserCreate

from app.core.auth import get_user_manager
from app.db.database import get_user_db, get_async_session, test_connection

app = typer.Typer()


@app.command()
def new_user(
    email: str,
    password: str,
    is_active: Optional[bool] = True,
    is_superuser: Optional[bool] = False,
    is_verified: Optional[bool] = False,
):
    data = {
        "email": email,
        "password": password,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "is_verified": is_verified,
    }
    typer.echo(f"Created")
    typer.echo(f"=======")
    for key, value in data.items():
        if key == "password":
            typer.echo(f"{key}:{len(value)*'*'}")
        else:
            typer.echo(f"{key}:{value}")

    async def _main():
        create = BaseUserCreate(
            email=email,
            password=password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )
        await test_connection()
        print("tested connection")
        session = await get_async_session().__anext__()
        user_db = await get_user_db(session).__anext__()
        manager = await get_user_manager(user_db).__anext__()
        await manager.create(create)

    asyncio.run(_main())


if __name__ == "__main__":
    app()
