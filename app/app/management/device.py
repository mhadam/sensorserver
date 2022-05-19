import asyncio

import typer
from fastapi_users.models import BaseUserDB

from app.api.dependencies.db import async_session
from app.core.auth import get_user_manager
from app.db.database import database, get_async_session, get_user_db
from app.db.repositories.device_auth import DeviceAuthRepository
from app.db.repositories.device_request import DeviceRequestRepository
from app.db.tables.device_auth import DeviceAuth as DeviceAuthTable
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.models.device_auth import DeviceAuthCreate

app = typer.Typer()


async def get_user(email: str) -> BaseUserDB:
    await database.connect()
    session = await get_async_session().__anext__()
    user_db = await get_user_db(session).__anext__()
    manager = await get_user_manager(user_db).__anext__()
    user: BaseUserDB = await manager.get_by_email(email)
    await database.disconnect()
    return user


@app.command()
def approve_device(device_id: str, email: str):
    data = {"device_id": device_id, "email": email}
    typer.echo(f"Added auth")
    typer.echo(f"=======")
    for key, value in data.items():
        typer.echo(f"{key}:{value}")

    async def _main():
        async with async_session() as session:
            request_repo = DeviceRequestRepository(DeviceRequestTable, session)
            device = await request_repo.get_device(device_id)
            if device:
                user = await get_user(email)
                auth_repo = DeviceAuthRepository(DeviceAuthTable, session)
                obj = DeviceAuthCreate(
                    **{
                        "device_id": device_id,
                        "ip_address": device.ip_address,
                        "user_id": user.id,
                    }
                )
                _ = await auth_repo.create(obj)
            await database.disconnect()

    asyncio.run(_main())


if __name__ == "__main__":
    app()
