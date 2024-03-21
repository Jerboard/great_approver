from aiogram.types import ChatJoinRequest, Message, CallbackQuery, ReplyKeyboardRemove, MessageEntity
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.enums.content_type import ContentType

import logging
import json

import db
import keyboards as kb
from init import dp, bot, ADMINS, CHANNEL_ID
from utils.entities_utils import recover_entities
from enums import BaseCB, KeyboardButtons, TextTypes


async def com_start_for_user(user_id: int):
    # text = ('Скорее забирай подарок курс "60 законов денег" в нашем канале:\n'
    #         '➡️ https://t.me/+vlvsa5AvvQEzOGFi')
    text_info = await db.get_text (channel_id=CHANNEL_ID, text_type=TextTypes.SECOND.value)
    entities = recover_entities (text_info.entities)
    if text_info.photo_id:
        await bot.send_photo (
            chat_id=user_id,
            photo=text_info.photo_id,
            caption=text_info.text,
            caption_entities=entities,
            parse_mode=None,
            protect_content=True,
            reply_markup=ReplyKeyboardRemove ())
    else:
        await bot.send_message(
            chat_id=user_id,
            text=text_info.text,
            entities=entities,
            parse_mode=None,
            protect_content=True,
            reply_markup=ReplyKeyboardRemove())


@dp.chat_join_request()
async def chat_join_request(request: ChatJoinRequest):
    # text = ('Вам подарок 🎁 за подписку на канал Анастасии А\n\n'
    #         'Привет, волшебница 🪄\n\n'
    #         'Дарим супер важный курс, с которого начинается денежная трансформация многих волшебниц 🔥\n\n'
    #         '💰 «60 законов денег» 💰\n\n'
    #         'Это 60 ежедневных аудио в закрытом телеграм-канале для увеличения дохода и исполнения желаний 💥\n\n'
    #         'После курса:\n\n'
    #         '- вы узнаете о самых эффективных и простых денежных законах\n'
    #         '- вам будет проще не нарушать законы денег и открыть новые возможности\n'
    #         '- сможете поменять свое денежное мышление и притянете изобилие\n\n'
    #         'Нажмите 👉 /start или кнопку "ПОЛУЧИТЬ ПОДАРОК" 👇 и получи доступ на курс ✨')

    text_info = await db.get_text(channel_id=CHANNEL_ID, text_type=TextTypes.FIRST.value)
    entities = recover_entities(text_info.entities)

    button_info = await db.get_text (channel_id=CHANNEL_ID, text_type=TextTypes.BUTTON.value)

    if text_info.photo_id:
        await request.answer_photo_pm(
            photo=text_info.photo_id,
            caption=text_info.text,
            caption_entities=entities,
            parse_mode=None,
            reply_markup=kb.get_stat_user_kb (text=button_info.text)
        )
    else:
        await request.answer_pm(
            text=text_info.text,
            entities=entities,
            parse_mode=None,
            reply_markup=kb.get_stat_user_kb(text=button_info.text)
        )
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
# @dp.message (lambda msg: msg.text == KeyboardButtons.SEND_PRICE.value, StateFilter(default_state))
@dp.message (StateFilter(default_state))
async def com_start(msg: Message):
    await com_start_for_user(user_id=msg.from_user.id)


# отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def sending_messages(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
