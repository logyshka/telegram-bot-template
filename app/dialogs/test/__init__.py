from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import Jinja

from app.dialogs.states import TestDialog
from app.dialogs.utils.getters import UnionGetter, StaticDataGetter, MiddlewareDataGetter
from app.services.database import UserRole


async def close(call, widget, manager: DialogManager):
    await manager.done({"test": 2})


# root = TplWindow(
#     template_path=r"test.jinja",
#     state=TestDialog.root
# )

root = Window(
    Jinja("Testing something"),
    state=TestDialog.root,
)

ui = Dialog(
    root,
)


__all__ = (
    "ui",
)
