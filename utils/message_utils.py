from aiogram.types import ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest

import db
import keyboards as kb
from datetime import datetime, timedelta
from init import bot, CHANNEL_ID, TZ, DATE_FORMAT
from utils.entities_utils import recover_entities
from enums import TextTypes


async def com_start_for_user(user_id: int):
    await db.update_user(user_id=user_id, is_active=True)
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


async def com_start_admin(user_id: int, message_id: int = None):
    users = await db.get_all_users ()

    current_date = datetime.now (TZ).date ()
    one_day_ago = current_date - timedelta (days=1)
    seven_days_ago = current_date - timedelta (days=7)

    count_active_user = 0
    all_users_7_days = 0
    active_users_7_days = 0
    all_users_1_day = 0
    active_users_1_day = 0
    all_users_today = 0
    active_users_today = 0
    for user in users:
        if user.is_active:
            count_active_user += 1

        if user.first_visit.date () > seven_days_ago:
            all_users_7_days += 1
            if user.is_active:
                active_users_7_days += 1

        if user.first_visit.date () == one_day_ago:
            all_users_1_day += 1
            if user.is_active:
                active_users_1_day += 1

        if user.first_visit.date () == current_date:
            all_users_today += 1
            if user.is_active:
                active_users_today += 1

    text = (f'<b>Весь период с 20.03.2024:</b>\n'
            f'Одобрил подписку: {len (users)}\n'
            f'Подписались на бот: {count_active_user}\n'
            f'<b>Последняя неделя с {seven_days_ago.strftime (DATE_FORMAT)}:</b>\n'
            f'Одобрил подписку: {all_users_7_days}\n'
            f'Подписались на бот: {active_users_7_days}\n'
            f'<b>Вчера:</b>\n'
            f'Одобрил подписку: {all_users_1_day}\n'
            f'Подписались на бот: {active_users_1_day}\n'
            f'<b>Сегодня:</b>\n'
            f'Одобрил подписку: {all_users_today}\n'
            f'Подписались на бот: {active_users_today}\n')
    if message_id:
        try:
            await bot.edit_message_text (
                chat_id=user_id,
                message_id=message_id,
                text=text,
                reply_markup=kb.get_admin_kb ())
        except TelegramBadRequest as ex:
            pass
    else:
        await bot.send_message (chat_id=user_id, text=text, reply_markup=kb.get_admin_kb ())
