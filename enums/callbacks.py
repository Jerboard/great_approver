import enum


class BaseCB(str, enum.Enum):
    SENDING_MESSAGES = 'sending_messages'
    CLOSE = 'close'
