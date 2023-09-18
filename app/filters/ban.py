from typing import *

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.services.database import User, UserRole


class BanFilter(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        user = await User.get_or_none(id=update.from_user.id)
        if not user:
            return False
        return user.is_banned
