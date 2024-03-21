from enum import Enum


class KeyboardButtons(str, Enum):
    SEND_PRICE = 'ПОЛУЧИТЬ ПОДАРОК'


class TextTypes(str, Enum):
    FIRST = 'first'
    SECOND = 'second'
    BUTTON = 'button'
