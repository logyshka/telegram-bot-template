from aiogram import Bot
from aiogram.types import User

from app.data.config import Config
from app.services.database import SubscriptionDuty


async def root_getter(bot: Bot, config: Config, **kwargs):
    all_ = await SubscriptionDuty.get_all(bot)
    return {
        "all": all_,
        "count": len(all_),
        "is_on": config.misc.need_required_sub
    }


async def request_subscribe_getter(bot: Bot, event_from_user: User, **kwargs):
    unsubscribed_all = await SubscriptionDuty.get_unsubscribed_all(
        bot=bot,
        user_id=event_from_user.id
    )

    return {
        "unsubscribed_all": unsubscribed_all
    }


__all__ = (
    "root_getter",
    "request_subscribe_getter",
)
