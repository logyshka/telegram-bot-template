from typing import *

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.data.config import Config
from app.services.database import SubscriptionDuty


class SubscriptionFilter(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery], bot: Bot, config: Config) -> bool:
        user_id = update.from_user.id

        channels = await SubscriptionDuty.get_all(bot=bot)

        if not config.misc.need_required_sub:
            return True

        for channel in channels:
            if not await channel.is_user_member(
                bot=bot,
                user_id=user_id
            ):
                return False

        return True
