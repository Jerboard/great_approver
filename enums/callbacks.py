import enum


class BaseCB(str, enum.Enum):
    SENDING_MESSAGES = 'sending_messages'
    STATISTIC_UPDATE = 'statistic_update'
    ADMIN_EDIT_TEXT = 'admin_edit_text'
    CLOSE = 'close'
