import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.utils.getters import *
from app.dialogs.states import MailingDialog, MailingForm
from app.dialogs.utils.widgets import PrevDialog, NextDialog
from .forms import forms
from .functions import *
from .getters import *


class SwitchToRoot(SwitchTo):
    def __init__(self, text: Text = Jinja("🚫 Отмена")):
        super().__init__(text, id="__root__", state=MailingDialog.menu_view)


root = Window(
    Jinja(
        "{% if completed == 0 %}"
        "<b>❌ Пока что не проведено ни одной рассылки</b>"
        "{% else %}"
        "<b>✉ Проведено рассылок: <code>{{ completed }}</code></b>\n"
        "<b>⌛ Средняя длительность: <code>{{ duration }}</code></b>\n"
        "<b>👤 Средний охват:\n<code>✅{{ succeed }} ❌{{ failed }} 👥{{ all_view }}</code></b>"
        "{% endif %}"
    ),
    SwitchTo(
        Jinja("📫 Запланированные ({{ planned_all }})",),
        id="planned_all",
        state=MailingDialog.planned_all_view
    ),
    Row(
        NextDialog(
            Jinja("▶ Провести раccылку"),
            state=MailingForm.message,
            on_click=on_choice_type,
            start_data=dict(is_planning=False)
        ),
        NextDialog(
            Jinja("🗓 Запланировать раccылку"),
            state=MailingForm.message,
            on_click=on_choice_type,
            start_data=dict(is_planning=True)
        ),
    ),
    PrevDialog(Jinja("⏪ Назад")),
    state=MailingDialog.menu_view,
    getter=root_getter,
)


planned_all = Window(
    Jinja(
        "{% if count == 0 %}"
        "<b>❌ На данный момент не запланировано ни одной рассылки</b>"
        "{% else %}"
        "<b>📫 На данный момент запланировано рассылок: <code>{{ count }}</code></b>"
        "{% endif %}"
    ),
    ScrollingGroup(
        Select(
            Jinja("#{{ item.id }}"),
            id="planned_one",
            item_id_getter=operator.attrgetter("id"),
            items="planned_all",
            on_click=show_planned_one
        ),
        width=1,
        height=5,
        hide_on_single_page=True,
        id="planned_all"
    ),
    SwitchToRoot(Jinja("⏪ Назад")),
    state=MailingDialog.planned_all_view,
    getter=planned_all_getter
)

planned_one = Window(
    Jinja(
        "<b>📫 Рассылка: <code>#{{ planned_one.id }}</code></b>\n"
        "<b>⏰ Рассылка будет через <code>{{ planned_one.next_run_time - now_time }}</code></b>\n"
    ),
    Row(
        Button(
            Const("👁 Показать сообщение"),
            id="mailing_preview",
            on_click=mailing_preview
        ),
        SwitchTo(
            Const("🚫 Отменить рассылку"),
            id="planned_cancellation",
            state=MailingDialog.planned_cancel
        )
    ),
    SwitchTo(
        Const("⏪ Назад"),
        id="to_planned_all",
        state=MailingDialog.planned_all_view
    ),
    state=MailingDialog.planned_one_view,
    getter=UnionGetter(
        DialogDataGetter("planned_one"),
        now_time_getter
    )
)

planned_cancellation = Window(
    Jinja("<b>❓ Вы уверены, что хотите отменить рассылку <code>#{{ planned_one.id }}</code></b>"),
    Row(
        Button(
            Const("✅ Да"),
            id="yes",
            on_click=cancel_planned
        ),
        SwitchTo(
            Const("❌ Нет"),
            id="no",
            state=MailingDialog.planned_all_view
        )
    ),
    state=MailingDialog.planned_cancel,
    getter=DialogDataGetter("planned_one")
)

ui = Dialog(
    root,
    planned_all,
    planned_one,
    planned_cancellation,
)

uis = (
    ui,
    *forms
)

__all__ = (
    "uis",
)
