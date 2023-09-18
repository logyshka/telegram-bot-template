from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.utils.widgets import NextDialog
from . import backup, mailing, search, statistics, subscription_duties
from .getters import *
from ..states import *
from ..utils.getters import MiddlewareDataGetter
from ...services.database import UserRole

to_root_btn = SwitchTo(
    Const("⏪ Назад"),
    id="to_root_btn",
    state=AdminDialog.menu_view
)

root = Window(
    Jinja(
        "<b>🥥 Добро пожаловать</b>\n\n"
        "<b>🔰 Ваша роль: <code>{{ user.role }}</code></b>"
    ),
    ScrollingGroup(
        NextDialog(
            Jinja("💾 Бэкап"),
            state=BackupDialog.menu_view,
            when=F["user"].role == UserRole.OWNER
        ),
        NextDialog(
            Jinja("✉ Рассылки"),
            state=MailingDialog.menu_view,
        ),
        NextDialog(
            Jinja("📢 Обязательные подписки"),
            state=SubscriptionDutyDialog.root
        ),
        NextDialog(
            Jinja("🔎 Поиск"),
            state=SearchDialog.menu_view
        ),
        NextDialog(
            Jinja("📊 Статистика"),
            state=StatisticsDialog.menu_view
        ),
        width=2,
        height=3,
        hide_pager=True,
        hide_on_single_page=True,
        id="admin_panel"
    ),
    NextDialog(
        Jinja("⌚ В главное меню"),
        state=UserDialog.root,
        save_prev=False
    ),
    state=AdminDialog.menu_view,
    getter=MiddlewareDataGetter("user")
)

ui = Dialog(
    root,
)

uis = (
    ui,
    *backup.uis,
    *mailing.uis,
    *search.uis,
    *statistics.uis,
    *subscription_duties.uis,
)

__all__ = (
    "uis",
)
