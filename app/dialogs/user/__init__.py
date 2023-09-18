from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from ..states import UserDialog, AdminDialog
from ..utils.widgets import NextDialog

root = Window(
    Jinja("⌚ Главное меню"),
    NextDialog(
        Jinja("🥥 К админке"),
        state=AdminDialog.menu_view,
        save_prev=False
    ),
    state=UserDialog.root
)


ui = Dialog(
    root,
)

uis = (
    ui,
)

__all__ = (
    "uis",
)
