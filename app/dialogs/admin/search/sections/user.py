from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.states import SearchDialog, SearchUserDialog
from app.dialogs.utils.functions import migrate_start_data
from app.dialogs.utils.getters import *
from app.dialogs.utils.getters import GetterField
from app.dialogs.utils.widgets import PrevDialog, NextDialog
from app.services.database import UserRole
from ..functions import *
from ..getters import *


user_id = Window(
    Jinja(
        "{% if error %}"
        "<b>⚠ Произошла ошибка: <code>{{ error }}.</code></b>\n\n"
        "{% endif %}"
        "<b>#️⃣ Введите <code>#ID</code> или <code>@username</code> пользователя:</b>"
    ),
    TextInput(
        id="user_id",
        on_success=on_user_id_input
    ),
    NextDialog(
        Jinja("🚫 Отмена"),
        state=SearchDialog.menu_view,
        save_prev=False
    ),
    state=SearchUserDialog.user_id,
    getter=DialogDataGetter("error")
)

user_view = Window(
    Jinja(
        "<b>⌚ Профиль <code>#{{ user.id }}</code></b>\n\n"
        "<b>👤 Имя пользователя: <i>@{{ user.username }}</i></b>\n"
        "<b>⚜ Роль: <code>{{ user.role }}</code></b>\n\n"
        "{% if user.is_banned %}"
        "<b>❗ Данный пользователь забанен</b>"
        "{% endif %}"
    ),
    Row(
        Button(
            Jinja(
                "{% if user.is_banned %}"
                "🔓 Разбанить"
                "{% else %}"
                "🔒 Забанить"
                "{% endif %}"
            ),
            id="ban_user",
            on_click=switch_user_ban,
            when=(
                ((F["admin"].role == UserRole.OWNER) & (F["user"].role != UserRole.OWNER))
                |
                ((F["admin"].role == UserRole.ADMIN) & (F["user"].role == UserRole.USER))
            )
        ),
        Button(
            Jinja(
                "{% if saved %}"
                "🖤 Удалить из избранного"
                "{% else %}"
                "❤ Сохранить в избранное"
                "{% endif %}"
            ),
            id="search_user_save",
            on_click=switch_user_bookmark
        )
    ),
    Row(
        Button(
            Jinja("⬆ Повысить до админа"),
            id="promote_user",
            on_click=promote_user,
            when=F["user"].role == UserRole.USER
        ),
        Button(
            Jinja("⬇ Понизить до пользователя"),
            id="unpromote_user",
            on_click=unpromote_user,
            when=F["user"].role == UserRole.ADMIN
        ),
        when=F["admin"].role == UserRole.OWNER
    ),
    SwitchTo(
        Jinja("🔄 Найти другого"),
        id="search_other_user",
        state=SearchUserDialog.user_id
    ),
    Row(
        NextDialog(
            Jinja("❤ В избранное ({{ bookmarks_count }})"),
            state=SearchDialog.bookmarks,
            save_prev=False
        ),
        NextDialog(
            Jinja("🔍 В меню поиска"),
            state=SearchDialog.menu_view,
            save_prev=False
        ),
    ),
    state=SearchUserDialog.user_view,
    getter=UnionGetter(
        DialogDataGetter("user"),
        MiddlewareDataGetter(
            GetterField(
                name="user",
                result_name="admin"
            )
        ),
        user_saved_getter,
        bookmarks_count_getter
    )
)

ui = Dialog(
    user_id,
    user_view,
    on_start=migrate_start_data
)

__all__ = (
    "ui",
)
