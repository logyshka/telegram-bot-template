from aiogram_dialog import DialogManager

from app.dialogs.utils.getters import AsyncStaticDataGetter
from app.services.database import SearchBookmark


async def user_saved_getter(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.dialog_data["user"].id
    return {
        "saved": await SearchBookmark.is_user_saved(user_id=user_id)
    }


async def bookmarks_count_getter(**kwargs):
    return {
        "bookmarks_count": await SearchBookmark.filter().count()
    }


async def bookmarks_getter(dialog_manager: DialogManager, **kwargs):
    bookmarks = SearchBookmark.filter()
    filter_ = dialog_manager.dialog_data.get("filter")

    if not filter_:
        filter_ = "ALL"
        dialog_manager.dialog_data["filter"] = filter_
    elif filter_ != "ALL":
        bookmarks = bookmarks.filter(section=filter_)

    return {
        "bookmarks": await bookmarks,
        "filter": filter_
    }


__all__ = (
    "user_saved_getter",
    "bookmarks_count_getter",
    "bookmarks_getter"
)
