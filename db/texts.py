import sqlalchemy as sa
import typing as t

from sqlalchemy.dialects.postgresql import ARRAY

from db.base import METADATA, begin_connection


class TextRow(t.Protocol):
    id: int
    channel_id: int
    text_type: str
    content_type: str
    text: str
    entities: list
    photo_id: str


TextTable = sa.Table(
    'texts',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('channel_id', sa.BigInteger),
    sa.Column('type', sa.String(255)),
    sa.Column('content_type', sa.String(255)),
    sa.Column('text_type', sa.String(255)),
    sa.Column('text', sa.Text),
    sa.Column('photo_id', sa.String(255)),
    sa.Column('entities', ARRAY(sa.String)),
)


# добавить текст
async def add_text(
        channel_id: int,
        text_type: str,
        content_type: str,
        text: str,
        entities: list,
        photo_id: str = None) -> None:
    query = TextTable.insert().values(
                    channel_id=channel_id,
                    text_type=text_type,
                    content_type=content_type,
                    text=text,
                    entities=entities,
                    photo_id=photo_id
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# обновить текст
async def update_text(
        channel_id: int,
        text_type: str,
        content_type: str,
        text: str,
        entities: list,
        photo_id: str = None) -> None:
    query = (TextTable.update().values(
        content_type=content_type,
        text=text,
        entities=entities,
        photo_id=photo_id)
             .where(TextTable.c.channel_id == channel_id, TextTable.c.text_type == text_type))
    async with begin_connection() as conn:
        await conn.execute(query)


# добавить текст
async def get_text(channel_id: int, text_type: str, ) -> TextRow:
    query = TextTable.select ().where (
        TextTable.c.channel_id == channel_id,
        TextTable.c.text_type == text_type)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()
