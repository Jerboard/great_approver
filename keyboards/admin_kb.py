from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from enums import BaseCB, TextTypes


def get_admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📯 Сделать рассылку', callback_data=BaseCB.SENDING_MESSAGES.value)],
        [InlineKeyboardButton(text='📝 Изменить текст приветствия',
                              callback_data=f'{BaseCB.ADMIN_EDIT_TEXT.value}:{TextTypes.FIRST.value}')],
        [InlineKeyboardButton(text='📝 Изменить текст подарка ',
                              callback_data=f'{BaseCB.ADMIN_EDIT_TEXT.value}:{TextTypes.SECOND.value}')],
        [InlineKeyboardButton(text='📝 Изменить название кнопки',
                              callback_data=f'{BaseCB.ADMIN_EDIT_TEXT.value}:{TextTypes.BUTTON.value}')],
    ])


def get_close_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗑 Отменить', callback_data=BaseCB.CLOSE.value)]
    ])