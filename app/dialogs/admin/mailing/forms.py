from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import *
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.utils.factories import time_factory
from app.dialogs.utils.getters import DialogDataGetter, UnionGetter, StartDataGetter
from app.dialogs.states import MailingForm
from app.dialogs.utils.widgets import PrevDialog
from .getters import now_time_getter
from .functions import on_get_message, on_choice_scope, on_choice_date, on_time_input, create_one, mailing_preview

message = Window(
    Jinja("<b>↪ Перешлите боту сообщение, которое хотите разослать.</b>"),
    MessageInput(on_get_message),
    PrevDialog(Jinja("🚫 Отмена")),
    state=MailingForm.message
)

scope = Window(
    Jinja("<b>👤 Выберите группу пользователей, которой будет отправлено сообщение.</b>"),
    Button(
        Jinja("♦ Все пользователи"),
        id="all_users",
        on_click=on_choice_scope
    ),
    Button(
        Jinja("♦ Админы"),
        id="admins",
        on_click=on_choice_scope
    ),
    Row(
        Back(Jinja("⏪ Назад")),
        PrevDialog(Jinja("🚫 Отмена")),
    ),
    state=MailingForm.scope
)

date = Window(
    Jinja(
        "<b>⏰ Текущее время: <code>{{ now_time }}</code></b>\n\n"
        "<b>🗓 Выберите дату проведения рассылки</b>"
    ),
    Calendar(
        id="on_choice_date",
        on_click=on_choice_date
    ),
    Row(
        Back(Jinja("⏪ Назад")),
        PrevDialog(Jinja("🚫 Отмена")),
    ),
    state=MailingForm.date,
    getter=now_time_getter
)

time = Window(
    Jinja(
        "<b>⏰ Текущее время: <code>{{ now_time }}</code></b>\n\n"
        "<b>🗓 Выбранная дата: <code>{{ date }}</code>\n\n</b>"
        "<b>⏰ Введите время проведения рассылки в формате:</b>\n"
        "<code>HH:MM</code>"
    ),
    TextInput(
        id="on_time_input",
        type_factory=time_factory,
        on_success=on_time_input,
    ),
    Row(
        Back(Jinja("⏪ Назад")),
        PrevDialog(Jinja("🚫 Отмена")),
    ),
    state=MailingForm.time,
    getter=UnionGetter(
        DialogDataGetter("date"),
        now_time_getter
    )
)

confirmation = Window(
    Jinja(
        "{% if is_planning %}"
        "<b>❓ Вы уверены, что хотите запланировать рассылку на <code>{{ run_date }}</code></b>"
        "{% else %}"
        "<b>❓ Вы уверены, что хотите провести рассылку</b>"
        "{% endif %}"
    ),
    Button(
        Jinja("👁 Показать сообщение"),
        id="mailing_preview",
        on_click=mailing_preview
    ),
    Row(
        Button(
            Jinja("✅ Да"),
            id="on_confirmation",
            on_click=create_one
        ),
        PrevDialog(Jinja("❌ Нет")),
    ),
    Back(Jinja("⏪ Назад")),
    state=MailingForm.confirmation,
    getter=UnionGetter(
        DialogDataGetter("run_date"),
        StartDataGetter("is_planning")
    )
)

form = Dialog(
    message,
    scope,
    date,
    time,
    confirmation
)

forms = (form,)

__all__ = ("forms",)
