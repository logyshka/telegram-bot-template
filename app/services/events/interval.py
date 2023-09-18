import logging
import os
import zipfile

from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.data.config import Config
from app.data.const import *


async def make_backup(bot: Bot, config: Config):
    files_to_backup = (
        CONFIG_FILE,
        DATABASE_FILE,
    )
    backup = zipfile.ZipFile(BACKUP_SUMMARY_FILE, "w")
    for file in files_to_backup:
        backup.write(
            filename=file,
            arcname=file.name
        )
    backup.close()
    await bot.send_document(
        chat_id=config.bot.owner_id,
        document=FSInputFile(
            path=BACKUP_SUMMARY_FILE
        ),
        caption="<b>🛡 Бэкап сохранён</b>"
    )
    os.remove(BACKUP_SUMMARY_FILE)
    logging.info("Backups were sent")


def register_interval_events(scheduler: AsyncIOScheduler, bot: Bot, config: Config):
    scheduler.add_job(
        id="backup",
        kwargs=dict(
            bot=bot,
            config=config
        ),
        func=make_backup,
        trigger=IntervalTrigger(
            hours=config.misc.backup_interval
        )
    )
