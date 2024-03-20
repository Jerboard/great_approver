from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from enums import KeyboardButtons


def get_stat_user_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [KeyboardButton(text=KeyboardButtons.SEND_PRICE.value)]
    ])
