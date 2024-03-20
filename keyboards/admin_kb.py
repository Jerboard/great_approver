from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from enums import BaseCB


def get_admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📯 Сделать рассылку', callback_data=BaseCB.SENDING_MESSAGES.value)]
    ])


def get_close_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗑 Отменить', callback_data=BaseCB.CLOSE.value)]
    ])