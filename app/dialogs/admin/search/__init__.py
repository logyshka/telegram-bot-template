import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from app.dialogs.states import SearchDialog, SearchUserDialog, AdminDialog
from app.dialogs.utils.widgets import NextDialog
from .functions import *
from .getters import *
from .sections import sections


class SwitchToRoot(SwitchTo):
    def __init__(self, text: Text = Jinja("🚫 Отмена")):
        super().__init__(text, id="__root__", state=SearchDialog.menu_view)


menu_view = Window(
    Jinja("<b>🔎 Меню поиска</b>"),
    Row(
        SwitchTo(
            Jinja("🔎 Начать поиск"),
            id="search",
            state=SearchDialog.search,
            on_click=set_departure
        ),
        SwitchTo(
            Jinja("❤ Избранное ({{ bookmarks_count }})"),
            id="bookmarks",
            state=SearchDialog.bookmarks
        ),
    ),
    NextDialog(
        Jinja("⏪ Назад"),
        state=AdminDialog.menu_view,
        save_prev=False
    ),
    state=SearchDialog.menu_view,
    getter=bookmarks_count_getter
)


bookmarks = Window(
    Jinja("<b>❤ Избранное</b>"),
    Button(
        Jinja("♦ Фильтр: {{ filter }}"),
        id="change_filter",
        on_click=change_filter
    ),
    ScrollingGroup(
        Select(
            Jinja("{{ item.section }} #{{ item.item_id }}"),
            id="bookmarks",
            items="bookmarks",
            item_id_getter=operator.attrgetter("id"),
            on_click=open_bookmark
        ),
        width=1,
        height=5,
        hide_on_single_page=True,
        id="bookmarks_container"
    ),
    SwitchToRoot(Jinja("⏪ Назад")),
    state=SearchDialog.bookmarks,
    getter=bookmarks_getter
)


search = Window(
    Jinja("<b>🔎 Что будем искать?</b>"),
    NextDialog(
        Jinja("👤 Пользователя"),
        state=SearchUserDialog.user_id
    ),
    SwitchToRoot(Jinja("⏪ Назад")),
    state=SearchDialog.search
)


ui = Dialog(
    menu_view,
    bookmarks,
    search,
)

uis = (
    ui,
    *sections
)

__all__ = (
    "uis",
)
