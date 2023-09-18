from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def root_getter(scheduler: AsyncIOScheduler, **kwargs):
    job = scheduler.get_job(job_id="backup")
    next_backup_time = job.next_run_time
    next_backup_time -= datetime.now(next_backup_time.tzinfo)
    next_backup_time = next_backup_time.seconds

    hours = next_backup_time // 3600
    next_backup_time %= 3600
    minutes = next_backup_time // 60
    next_backup_time %= 60
    seconds = next_backup_time

    return {
        "next_time": "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    }


__all__ = (
    "root_getter",
)