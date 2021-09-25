import asyncio
from typing import Optional

import typer
from fastapi_users.models import BaseUserCreate

from app.api.dependencies.auth import fastapi_users
from app.db.database import database

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
        await database.connect()
        create = BaseUserCreate(
            email=email,
            password=password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )
        await fastapi_users.create_user(create)
        await database.disconnect()

    asyncio.run(_main())


if __name__ == "__main__":
    app()
