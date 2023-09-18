from aiogram import Dispatcher

from .ban import BanFilter
from .role import RoleFilter, OwnerFilter, AdminFilter
from .subscription import SubscriptionFilter
from .username import UsernameRequiredFilter


def register_filters(dispatcher: Dispatcher):
    filters = (
        ~BanFilter(),
    )
    dispatcher.message.filter(*filters)
    dispatcher.callback_query.filter(*filters)


__all__ = (
    "RoleFilter",
    "OwnerFilter",
    "AdminFilter",
    "UsernameRequiredFilter",
    "SubscriptionFilter",
    "BanFilter",
    "register_filters",
)
