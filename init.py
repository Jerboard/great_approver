from aiogram import Dispatcher
from aiogram import Bot
from aiogram.enums import ParseMode

from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine

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
bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)

DEBUG = bool(int(getenv('DEBUG')))

ENGINE = create_async_engine(url=getenv('DB_URL'))

admins_str = getenv('ADMINS')
ADMINS = json.loads(admins_str)
