from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import *
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.states import BackupForm
from app.dialogs.utils.widgets import PrevDialog
from .functions import on_file_input, on_accept_input

file = Window(
    Jinja("<b>⬆ Отправьте боту файл <code>backup.zip</code></b>"),
    MessageInput(
        func=on_file_input,
        content_types=ContentType.DOCUMENT
    ),
    PrevDialog(Jinja("🚫 Отмена")),
    state=BackupForm.file
)

confirmation = Window(
    Jinja("<b>❓ Вы уверены, что хотите использовать данный бэкап</b>"),
    Row(
        PrevDialog(
            Jinja("✅ Да"),
            on_click=on_accept_input
        ),
        PrevDialog(Jinja("❌ Нет"))
    ),
    state=BackupForm.confirmation
)

form = Dialog(
    file,
    confirmation
)

forms = (
    form,
)

__all__ = (
    "forms",
)
