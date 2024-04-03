from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from datetime import datetime

import logging
import traceback
import os

from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine
from pytz import timezone

import json
import asyncio


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop()
dp = Dispatcher()
TOKEN = getenv("TOKEN")
# TOKEN = '7181274585:AAEPJ_CXjhKFR3CiLhV8W9AS_8KmHej7JmI'
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

DEBUG = bool(int(getenv('DEBUG')))

ENGINE = create_async_engine(url=getenv('DB_URL'))

admins_str = getenv('ADMINS')
ADMINS = json.loads(admins_str)
CHANNEL_ID = -1002095723756
TZ = timezone('Europe/Moscow')
DATE_FORMAT = '%d.%m.%Y'


async def set_main_menu() -> None:
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Обновить бот'),
    ]
    await bot.set_my_commands (main_menu_commands)


def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('bot_logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')

    message = f'================================\n{message}\n================================'
    if with_traceback:
        ex_traceback = traceback.format_exc()
        logging.warning(f'{now}\n{ex_traceback}\n{message}')
    else:
        logging.warning(f'{now}\n{message}')
