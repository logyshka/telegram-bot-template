from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import *
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.utils.getters import DialogDataGetter
from app.dialogs.states import SubscriptionDutyForm
from app.dialogs.utils.widgets import PrevDialog
from .functions import create_duty, on_channel_info_input

channel_info = Window(
    Jinja(
        "{% if error %}"
        "<b>⚠ Ошибка: <code>{{ error }}</code></b>\n\n"
        "{% endif %}"
        "<b>❗ Перешлите сообщение из желаемого канала, либо отправьте id канала.</b>\n\n"
        "<code>❗ Бот должен быть админом канала</code>"
    ),
    MessageInput(
        func=on_channel_info_input
    ),
    PrevDialog(Jinja("🚫 Отмена")),
    state=SubscriptionDutyForm.channel_info,
    getter=DialogDataGetter("error")
)

confirmation = Window(
    Jinja("<b>❓ Вы уверены, что хотите добавить данный канал</b>"),
    Row(
        PrevDialog(
            Jinja("✅ Да"),
            on_click=create_duty
        ),
        PrevDialog(Jinja("❌ Нет")),
    ),
    state=SubscriptionDutyForm.confirmation
)

form = Dialog(
    channel_info,
    confirmation
)

forms = (
    form,
)

__all__ = (
    "forms",
)
