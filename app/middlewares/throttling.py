from typing import *

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache

from app.data.config import Config
from app.services.database import User


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, config: Config):
        self.cache = TTLCache(maxsize=10_000, ttl=config.misc.throttling_rate)

    async def __call__(
        self,
        handler: Callable[[Union[CallbackQuery, Message], Dict[str, Any]], Awaitable[Any]],
        update: Union[CallbackQuery, Message],
        data: Dict[str, Any],
    ) -> Any:
        user_id = update.from_user.id

        if user_id in self.cache:
            return

        self.cache[user_id] = None
        data["user"] = await User.get_or_none(id=user_id)
        return await handler(update, data)


def register_middleware(dp: Dispatcher, config: Config):
    throttling_middleware = ThrottlingMiddleware(config=config)
    dp.message.middleware(throttling_middleware)
    dp.callback_query.middleware(throttling_middleware)

