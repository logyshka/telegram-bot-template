from aiogram.types import Chat

from app.services.database import User, UserRole


async def get_user(event_chat: Chat, **kwargs):
    user: User = await User.get_or_none(id=event_chat.id)

    return {
        "user": user,
        "UserRole": UserRole
    }


__all__ = (
    "get_user",
)
