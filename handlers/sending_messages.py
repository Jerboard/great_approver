from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

import logging

import db
import keyboards as kb
from init import dp, bot
from enums import BaseCB


# начать рассылку
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.SENDING_MESSAGES.value))
async def sending_messages(cb: CallbackQuery, state: FSMContext):
    text = 'Отправьте сообщение для пользователей'
    await state.set_state(BaseCB.SENDING_MESSAGES)
    await cb.message.answer(text, reply_markup=kb.get_close_kb())


# отправить сообщения
@dp.message (StateFilter(BaseCB.SENDING_MESSAGES))
async def com_start(msg: Message, state: FSMContext):
    await state.clear ()
    sent = await msg.answer('⏳')

    users = await db.get_all_users ()
    counter = 0
    for user in users:
        try:
            if msg.content_type == ContentType.TEXT:
                await bot.send_message (chat_id=user.user_id, text=msg.text, entities=msg.entities, parse_mode=None)

            elif msg.content_type == ContentType.PHOTO:
                await bot.send_photo (
                    chat_id=user.user_id,
                    photo=msg.photo [-1].file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            elif msg.content_type == ContentType.VIDEO:
                await bot.send_video (
                    chat_id=user.user_id,
                    video=msg.video.file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            elif msg.content_type == ContentType.VIDEO_NOTE:
                await bot.send_video_note (
                    chat_id=user.user_id,
                    video_note=msg.video_note.file_id,
                )

            elif msg.content_type == ContentType.VOICE:
                await bot.send_voice (
                    chat_id=user.user_id,
                    voice=msg.voice.file_id,
                )

            elif msg.content_type == ContentType.ANIMATION:
                await bot.send_animation (
                    chat_id=user.user_id,
                    animation=msg.animation.file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            else:
                await msg.answer ('❌ Ни одно сообщение не отправлено. Неподдерживаемый формат сообщения')
                break

            counter += 1
        except Exception as ex:
            logging.warning(f'Сообщение не отправлено {ex}')
            pass

    end_text = f'✅ Сообщение отправлено {counter} пользователям'
    await sent.edit_text(text=end_text)

