from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
import typing as t

from init import ENGINE

METADATA = sa.MetaData()


def begin_connection() -> t.AsyncContextManager [AsyncConnection]:
    ENGINE.connect ()
    return ENGINE.begin ()


async def init_models():
    async with ENGINE.begin () as conn:
        await conn.run_sync (METADATA.create_all)
