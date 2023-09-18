import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.data.config import *
from app.data.const import *
from app.dialogs import register_dialogs
from app.handlers import register_handlers
from app.services.events import *
from app.utils.arguments import *


async def main():
    coloredlogs.install(level=logging.INFO)

    await use_arguments()

    config = parse_config(config_file=CONFIG_FILE)

    session = AiohttpSession()

    bot = Bot(
        token=config.bot.token,
        parse_mode=ParseMode.HTML,
        session=session
    )

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler()

    register_once_events(dispatcher=dp)
    register_interval_events(
        scheduler=scheduler,
        bot=bot,
        config=config
    )

    scheduler.start()

    context_kwargs = {
        "config": config,
        "scheduler": scheduler,
        "session": session
    }
    register_handlers(dispatcher=dp)
    register_dialogs(dispatcher=dp)

    await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")


