import sqlalchemy as sa
import typing as t

from datetime import datetime

from db.base import METADATA, begin_connection


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: int
    username: int
    first_visit: datetime
    channel_id: int
    is_active: bool


UserTable = sa.Table(
    'users',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('first_visit', sa.DateTime),
    sa.Column('channel_id', sa.BigInteger),
    sa.Column('is_active', sa.Boolean, default=False),
)


# сохраняет данные пользователя
async def add_user(user_id: int, full_name: str, username: str, channel_id: int) -> None:
    now = datetime.now ()
    async with begin_connection() as conn:
        result = await conn.execute(UserTable.select().where(UserTable.c.user_id == user_id))
        user = result.first()
        if not user:
            await conn.execute(
                UserTable.insert().values(
                    user_id=user_id,
                    full_name=full_name,
                    username=username,
                    first_visit=now,
                    channel_id=channel_id,
                )
            )


async def update_user(user_id: int, is_active: bool) -> None:
    async with begin_connection() as conn:
        await conn.execute(UserTable.update().where(UserTable.c.user_id == user_id).values(is_active=is_active))


# возвращает всех пользователей
async def get_all_users() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute(UserTable.select())
    return result.all()
