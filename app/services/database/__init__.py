import contextlib
import logging
import shutil
from pathlib import Path

from aerich import Command
from aerich.exceptions import NotSupportError
from aiogram import Bot
from click import Abort
from tortoise import Tortoise

from app.data.config import Config
from .enums import *
from .functions import *


def prepare_orm(migration_dir: Path, database_file: Path):
    if not database_file.exists() and migration_dir.exists():
        shutil.rmtree(migration_dir, True)
        logging.info("Previous migrations were deleted")


async def init_models(tortoise_config: dict, migration_dir: Path):
    command = Command(
        tortoise_config=tortoise_config,
        app="models",
        location=str(migration_dir)
    )
    await command.init()
    try:
        await command.init_db(safe=True)
    except FileExistsError:
        try:
            with contextlib.suppress(Abort):
                await command.migrate()
        except NotSupportError as e:
            logging.error(e)
    await command.upgrade()


async def init_orm(tortoise_config: dict) -> None:
    await Tortoise.init(config=tortoise_config)
    logging.info(f"Tortoise-ORM started, {Tortoise.apps}")


async def close_orm() -> None:
    await Tortoise.close_connections()
    logging.info("Tortoise-ORM shutdown")


async def create_static_orm(config: Config, bot: Bot):
    await User.create_static(config=config, bot=bot)


__all__ = (
    "prepare_orm",
    "create_static_orm",
    "init_models",
    "init_orm",
    "close_orm",
    "User",
    "UserRole",
    "MailingLog",
    "PlannedMailing",
    "SubscriptionDuty",
    "SearchBookmark",
    "SearchSection",
)
