import logging
import asyncio
import sys

from init import DEBUG, bot, set_main_menu, log_error
from handlers import dp
from db.base import init_models


async def main() -> None:
    await init_models()
    await set_main_menu()
    log_error('start', with_traceback=False)
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s", filename='log.log')
    asyncio.run(main())
