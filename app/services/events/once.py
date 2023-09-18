import logging
from dataclasses import dataclass
from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiohttp import ClientSession
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from tortoise.queryset import QuerySet

from app.data.config import Config
from app.data.const import *
from app.filters import register_filters
from app.middlewares import *
from app.services.database import *
from app.utils.commands import *


@dataclass
class MailConfig:
    bot: Bot = None
    message: Message = None
    initiator_id: int = None
    scope: QuerySet[User] = None


async def mail(mail_config: MailConfig):
    start_time = datetime.now()
    log: MailingLog = await MailingLog.create()

    await mail_config.bot.send_message(
        chat_id=mail_config.initiator_id,
        text=f"<b>❗ Рассылка началась</b>\n"
    )

    for user in await mail_config.scope:
        try:
            await mail_config.message.copy_to(
                chat_id=user.id,
                reply_markup=mail_config.message.reply_markup
            )
            log.scope_succeed += 1
        except Exception:
            log.scope_failed += 1

    log.scope_all = log.scope_failed + log.scope_succeed
    log.duration = (datetime.now() - start_time).seconds
    await log.save()

    await mail_config.bot.send_message(
        chat_id=mail_config.initiator_id,
        text=f"<b>❗ Рассылка завершена</b>\n\n"
             f"<b>⌛ Длительность: {MailingLog.format_duration(log.duration)}</b>\n"
             f"<b>👤 Охват: <code>\n✅{log.scope_succeed} ❌{log.scope_failed} 👥{log.scope_all}</code></b>"
    )


async def plan_mail(
        mail_config: MailConfig,
        run_date: datetime,
        scheduler: AsyncIOScheduler
) -> Job:
    return scheduler.add_job(
        func=mail,
        trigger=DateTrigger(
            run_date=run_date,
            timezone=run_date.tzinfo
        ),
        kwargs=dict(
            mail_config=mail_config
        ),
        name="mail"
    )


async def notify_owner(
        bot: Bot,
        text: str,
        config: Config
) -> None:
    try:
        await bot.send_message(
            chat_id=config.bot.owner_id,
            text=text
        )
    except Exception:
        pass


async def save_jobs(scheduler: AsyncIOScheduler) -> None:
    for job in scheduler.get_jobs():
        if job.name == "mail":
            mail_config = job.kwargs["mail_config"]
            await PlannedMailing.create(
                message=mail_config.message,
                scope=mail_config.scope,
                run_date=job.trigger.run_date,
                initiator_id=mail_config.initiator_id
            )
            logging.info(f"Mailing job saved. {job}")


async def restart_jobs(
        scheduler: AsyncIOScheduler,
        bot: Bot
) -> None:
    for mailing in await PlannedMailing.get_all():
        mail_config = MailConfig(
            bot=bot,
            scope=mailing.scope,
            message=mailing.message,
            initiator_id=mailing.initiator_id,
        )
        await plan_mail(
            mail_config=mail_config,
            run_date=mailing.run_date,
            scheduler=scheduler
        )
        await mailing.delete()


async def on_startup(
        dispatcher: Dispatcher,
        bot: Bot,
        config: Config,
        scheduler: AsyncIOScheduler
) -> None:
    tortoise_config = config.database.get_tortoise_config(DATABASE_FILE)
    logging.info(tortoise_config)

    prepare_orm(
        migration_dir=MIGRATION_DIR,
        database_file=DATABASE_FILE
    )
    await init_orm(tortoise_config=tortoise_config)
    await init_models(
        tortoise_config=tortoise_config,
        migration_dir=MIGRATION_DIR
    )

    await create_static_orm(
        config=config,
        bot=bot
    )

    await restart_jobs(
        scheduler=scheduler,
        bot=bot
    )

    register_filters(dispatcher=dispatcher)

    register_middlewares(
        dispatcher=dispatcher,
        config=config
    )

    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "on",
        False: "off",
    }

    logging.info(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.info(f"Inline Mode - {states[bot_info.supports_inline_queries]}")

    logging.warning("Starting bot...")

    await setup_bot_commands(
        bot=bot,
        config=config
    )
    await notify_owner(
        bot=bot,
        text="<b>✅ Бот был успешно запущен!</b>",
        config=config
    )


async def on_shutdown(
        dispatcher: Dispatcher,
        bot: Bot,
        config: Config,
        session: ClientSession,
        scheduler: AsyncIOScheduler
) -> None:
    logging.warning("Stopping bot...")
    await save_jobs(scheduler)
    await notify_owner(
        bot=bot,
        text="<b>❌ Бот был выключен!</b>",
        config=config
    )
    await remove_bot_commands(
        bot=bot,
        config=config
    )
    await dispatcher.fsm.storage.close()
    await close_orm()
    await dispatcher.stop_polling()
    await session.close()


def register_once_events(dispatcher: Dispatcher):
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
