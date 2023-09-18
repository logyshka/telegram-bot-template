from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.data.const import TZ_INFO
from app.services.database import MailingLog


async def root_getter(scheduler: AsyncIOScheduler, **kwargs):
    scope = await MailingLog.get_average_scope()
    completed = await MailingLog.get_count()
    duration = await MailingLog.get_average_duration()
    planned = len([i for i in scheduler.get_jobs() if i.name == "mail"])
    return {
        "completed": completed,
        "duration": duration,
        "planned_all": planned,
        "all_view": scope[0],
        "succeed": scope[1],
        "failed": scope[2],
    }


async def planned_all_getter(scheduler: AsyncIOScheduler, **kwargs):
    planned_mailings = [i for i in scheduler.get_jobs() if i.name == "mail"]

    return {
        "planned_all": planned_mailings,
        "count": len(planned_mailings)
    }


async def now_time_getter(**kwargs):
    return {
        "now_time": datetime.now(tz=TZ_INFO).replace(microsecond=0)
    }


__all__ = (
    "root_getter",
    "planned_all_getter",
    "now_time_getter"
)
