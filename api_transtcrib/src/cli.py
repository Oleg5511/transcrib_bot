import asyncio

import typer
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.config import get_settings
from db.postgres import async_session
from models import Role
from models.models import User

config = get_settings()
app = typer.Typer()


async def actions(user: User, role_name: str):
    """Функция регистрирует пользователя, записывая его данные в БД"""
    async with async_session() as db:
        try:
            # Создали роль
            user_role = Role(name=role_name)
            db.add(user_role)
            await db.commit()
            await db.refresh(user_role)

            # Добавили пользователя
            db.add(user)
            await db.commit()

            # Связали роль и пользователя
            statement = (
                select(User).where(User.id == user.id).options(selectinload(User.roles))
            )
            user = (await db.execute(statement)).scalars().first()
            user.roles.append(user_role)
            await db.commit()

        except Exception as ex:
            await db.rollback()
            raise Exception(f"Error {repr(ex)=}")
        finally:
            await db.close()


@app.command()
def create_superuser(
    email: str,
    password: str,
    first_name: str | None = None,
    last_name: str | None = None,
):
    """Создает суперпользователя в системе"""

    print(f"Start creating Superuser")
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    asyncio.run(actions(user=user, role_name=config.admin_role_name))
    print(f"Finished creating Superuser")


if __name__ == "__main__":
    app()

    # Ввести команду учитывая путь до файла
    # python cli.py admin@admin.com password
