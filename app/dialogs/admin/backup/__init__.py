from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.states import BackupDialog, BackupForm
from app.dialogs.utils.widgets import PrevDialog, NextDialog
from .forms import *
from .functions import *
from .getters import *

root = Window(
    Jinja("<b>💾 Следующий бэкап через <code>{{ next_time }}</code></b>"),
    Button(
        Const("⬇ Получить бэкап"),
        id="make_backup",
        on_click=make_backup
    ),
    NextDialog(
        Jinja("📀 Использовать бэкап"),
        state=BackupForm.file
    ),
    PrevDialog(Jinja("⏪ Назад")),
    state=BackupDialog.menu_view,
    getter=root_getter
)

ui = Dialog(
    root,
)

uis = (
    ui,
    *forms
)

__all__ = (
    "uis",
)
