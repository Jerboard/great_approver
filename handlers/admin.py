from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp, CHANNEL_ID
from utils.entities_utils import save_entities
from utils.message_utils import com_start_admin
from enums import BaseCB, TextTypes


# начать рассылку
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.ADMIN_EDIT_TEXT.value))
async def admin_edit_text(cb: CallbackQuery, state: FSMContext):
    _, text_type = cb.data.split(':')

    if text_type == TextTypes.FIRST.value:
        text = 'Отправьте сообщение для приветствия'
    elif text_type == TextTypes.SECOND.value:
        text = 'Отправьте сообщение для подарка'
    else:
        text = 'Отправьте сообщение для кнопки'

    await state.set_state(BaseCB.ADMIN_EDIT_TEXT)
    await state.update_data(data={'text_type': text_type})
    await cb.message.answer(text=text, reply_markup=kb.get_close_kb())


# сохранить текст
@dp.message (StateFilter(BaseCB.ADMIN_EDIT_TEXT))
async def admin_save_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear ()

    text = msg.text if msg.text else msg.caption
    entities = msg.entities if msg.entities else msg.caption_entities
    photo_id = msg.photo [-1].file_id if msg.photo else None

    await db.update_text(
        channel_id=CHANNEL_ID,
        text_type=data['text_type'],
        content_type=msg.content_type,
        text=text,
        entities=save_entities(entities),
        photo_id=photo_id
    )

    await msg.answer('Текст успешно обновлён')


# обновить стату
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.STATISTIC_UPDATE.value))
async def admin_edit_text(cb: CallbackQuery):
    await com_start_admin(user_id=cb.from_user.id, message_id=cb.message.message_id)
    await cb.answer('Данные обновлены')