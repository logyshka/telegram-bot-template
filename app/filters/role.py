from typing import *

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.services.database import User, UserRole


class RoleFilter(Filter):
    def __init__(self, *roles: UserRole, in_: bool = True) -> None:
        self.roles = roles
        self.in_ = in_

    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        user = await User.get_or_none(id=update.from_user.id)
        if not user:
            return False
        return (user.role in self.roles) is self.in_


class OwnerFilter(RoleFilter):
    def __init__(self):
        super().__init__(UserRole.OWNER)


class AdminFilter(RoleFilter):
    def __init__(self):
        super().__init__(UserRole.OWNER, UserRole.ADMIN)
