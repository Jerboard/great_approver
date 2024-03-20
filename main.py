import logging
import asyncio
import sys

from init import DEBUG, bot
from handlers import dp
from db.base import init_models


async def main() -> None:
    await init_models()
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s", filename='log.log')
    asyncio.run(main())
