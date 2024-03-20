from aiogram.types import ChatJoinRequest, Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.enums.content_type import ContentType

import logging

import db
import keyboards as kb
from init import dp, bot, ADMINS
from enums import BaseCB, KeyboardButtons


async def com_start_for_user(user_id: int):
    text = ('Скорее забирай подарок курс "60 законов денег" в нашем канале:\n'
            '➡️ https://t.me/+vlvsa5AvvQEzOGFi')
    await bot.send_message(
        chat_id=user_id,
        text=text,
        protect_content=True,
        reply_markup=ReplyKeyboardRemove())


@dp.chat_join_request()
async def chat_join_request(request: ChatJoinRequest):
    text = ('Вам подарок 🎁 за подписку на канал Анастасии А\n\n'
            'Привет, волшебница 🪄\n\n'
            'Дарим супер важный курс, с которого начинается денежная трансформация многих волшебниц 🔥\n\n'
            '💰 «60 законов денег» 💰\n\n'
            'Это 60 ежедневных аудио в закрытом телеграм-канале для увеличения дохода и исполнения желаний 💥\n\n'
            'После курса:\n\n'
            '- вы узнаете о самых эффективных и простых денежных законах\n'
            '- вам будет проще не нарушать законы денег и открыть новые возможности\n'
            '- сможете поменять свое денежное мышление и притянете изобилие\n\n'
            'Нажмите 👉 /start или кнопку "ПОЛУЧИТЬ ПОДАРОК" 👇 и получи доступ на курс ✨')

    await request.answer_pm(text, reply_markup=kb.get_stat_user_kb())
    try:
        await request.approve()
    except Exception as ex:
        text = (f'‼️ Не смок одобрить запрос\n'
                f'Пользователь: {request.from_user.full_name} ({request.from_user.username})\n'
                f'{ex}')
        for admin_id in ADMINS:
            await bot.send_message(chat_id=admin_id, text=text)

    finally:
        await db.add_user(
            user_id=request.from_user.id,
            full_name=request.from_user.full_name,
            username=request.from_user.username,
            channel_id=request.chat.id
        )


# старт
@dp.message (CommandStart())
async def com_start(msg: Message):
    if msg.from_user.id in ADMINS:
        users = await db.get_all_users()
        text = f'<b>Всего пользователей:</b> {len(users)}'
        await msg.answer(text, reply_markup=kb.get_admin_kb())
    else:
        await com_start_for_user(user_id=msg.from_user.id)


# старт по кнопке
@dp.message (lambda msg: msg.text == KeyboardButtons.SEND_PRICE.value, StateFilter(default_state))
async def com_start(msg: Message):
    await com_start_for_user(user_id=msg.from_user.id)


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


# отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def sending_messages(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
