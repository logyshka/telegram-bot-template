from typing import *

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.services.database import User


class UsernameRequiredFilter(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        return update.from_user.username is not None

class UsernameNotMatchFilter(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        user = await User.get_or_none(id=update.from_user.id)
        return user.username != update.from_user.username
