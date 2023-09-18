from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Select, SwitchTo

from app.dialogs.states import SearchDialog, SearchUserDialog
from app.dialogs.utils.widgets import NextDialog
from app.services.database import User, SearchBookmark, SearchSection, UserRole


async def on_user_id_input(msg: Message, widget: TextInput, manager: DialogManager, user_id: str):
    if len(user_id) < 2:
        await manager.update(dict(error="id или username слишком короткие"))
    elif user_id[0] == "@" or user_id[0] == "#":
        user = await User.search_user(user_id=user_id)
        if user is None:
            await manager.update(dict(error="такого пользователя не существует"))
        else:
            manager.dialog_data.update(
                dict(
                    user=user,
                    admin=manager.middleware_data["user"]
                )
            )
            await manager.switch_to(SearchUserDialog.user_view)
    else:
        await manager.update(dict(error="первым символом должен быть либо \"@\", либо \"#\""))


async def switch_user_ban(call: CallbackQuery, widget: Button, manager: DialogManager):
    user = manager.dialog_data["user"]
    user.is_banned = not user.is_banned
    await user.save()
    await manager.update(
        {
            "user": user
        }
    )


async def switch_user_bookmark(call: CallbackQuery, widget: Button, manager: DialogManager):
    user = manager.dialog_data["user"]
    saved = await SearchBookmark.switch_user(user_id=user.id)
    await manager.update(
        {
            "saved": saved
        }
    )


async def promote_user(call: CallbackQuery, widget: Button, manager: DialogManager):
    user = manager.dialog_data["user"]
    user.role = UserRole.ADMIN
    await user.save()
    await manager.update(
        {
            "user": user
        }
    )


async def unpromote_user(call: CallbackQuery, widget: Button, manager: DialogManager):
    user = manager.dialog_data["user"]
    user.role = UserRole.USER
    await user.save()
    await manager.update(
        {
            "user": user
        }
    )


async def open_bookmark(call: CallbackQuery, widget: Select, manager: DialogManager, bookmark_id: str):
    state = None
    bookmark = await SearchBookmark.get_or_none(id=bookmark_id)

    start_data = {}

    if bookmark.section == SearchSection.USER:
        state = SearchUserDialog.user_view
        start_data["user"] = await User.get_or_none(id=bookmark.item_id)

    await NextDialog.open(
        manager=manager,
        state=state,
        start_data=start_data,
        save_prev=False
    )


async def change_filter(call: CallbackQuery, widget: Button, manager: DialogManager):
    filter_ = manager.dialog_data.get("filter")

    filters: list[SearchSection] = [i for i in SearchSection]

    if filter_ == "ALL":
        filter_ = filters[0]

    else:
        length = len(filters)

        for i in range(length):
            if filters[i] == filter_:
                if i + 1 == length:
                    filter_ = "ALL"
                else:
                    filter_ = filters[i + 1]

                break

    manager.dialog_data["filter"] = filter_


async def set_departure(call: CallbackQuery, widget: SwitchTo, manager: DialogManager):
    manager.dialog_data["departure"] = manager.current_context().state


async def open_departure(call: CallbackQuery, widget: Button, manager: DialogManager):
    departure = manager.dialog_data.get("departure")
    if departure:
        await manager.switch_to(departure)


__all__ = (
    "on_user_id_input",
    "switch_user_ban",
    "switch_user_bookmark",
    "promote_user",
    "unpromote_user",
    "open_bookmark",
    "change_filter",
    "set_departure",
    "open_departure",
)
