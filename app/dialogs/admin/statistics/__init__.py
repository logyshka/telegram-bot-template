from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import *

from app.dialogs.states import StatisticsDialog
from app.dialogs.utils.widgets import PrevDialog
from .functions import *
from .getters import *

menu_view = Window(
    Jinja("<b>📊 Выберите раздел статистики:</b>"),
    ScrollingGroup(
        SwitchTo(
            Jinja("👤 Пользовательская"),
            id="user",
            state=StatisticsDialog.user
        ),
        width=2,
        height=3,
        hide_pager=True,
        hide_on_single_page=True,
        id="admin"
    ),
    PrevDialog(Jinja("⏪ Назад")),
    state=StatisticsDialog.menu_view
)

user = Window(
    DynamicMedia("graphic"),
    Jinja(
        "<u><b>👤 Пользовательская статистика</b></u>\n"
        "<b>├За указанный период: <code>{{ users_part_count }}</code></b>\n"
        "<b>└За всё время: <code>{{ users_all_count }}</code></b>\n"  # ├└
    ),
    Button(
        Jinja("📑 Тип графика: {{ graphic_name }}"),
        id="switch_user_graphic",
        on_click=switch_user_graphic,
    ),
    SwitchTo(
        Jinja("⏪ Назад"),
        id="user",
        state=StatisticsDialog.menu_view
    ),
    state=StatisticsDialog.user,
    getter=graphic_getter
)

ui = Dialog(
    menu_view,
    user,
)

uis = (
    ui,
)

__all__ = (
    "uis",
)
