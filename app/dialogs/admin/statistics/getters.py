from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from .functions import *


async def graphic_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    graphic_methods = {
        "user_income_week": (get_user_income_week, "Недельный"),
        "user_income_month": (get_user_income_month, "Месячный"),
    }
    graphic_id = dialog_manager.dialog_data.get("graphic_id") or "user_income_week"
    path, users_part_count = await graphic_methods[graphic_id][0]()
    graphic_name = graphic_methods[graphic_id][1]
    graphic = MediaAttachment(
        type=ContentType.PHOTO,
        path=path
    )
    return {
        "graphic": graphic,
        "graphic_name": graphic_name,
        "users_all_count": await User.filter().count(),
        "users_part_count": users_part_count
    }
