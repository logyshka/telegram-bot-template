import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import *
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *

from .forms import *
from .functions import *
from .getters import *
from app.dialogs.utils.getters import *
from ...states import SubscriptionDutyDialog, SubscriptionDutyForm
from app.dialogs.utils.widgets import PrevDialog, NextDialog


class SwitchToRoot(SwitchTo):
    def __init__(self, text: Text = Jinja("🚫 Отмена")):
        super().__init__(text, id="__root__", state=SubscriptionDutyDialog.root)


root = Window(
    Jinja(
        "<b>❗ Здесь вы можете добавить добавить каналы, подписка на которые будет являться обязательной для использования бота</b>\n\n"
        "{% if count == 0 %}"
        "<b>❌ Пока не было добавлено ни одного канала</b>"
        "{% else %}"
        "<b>📢 Добавлено каналов: <code>{{ count }}</code></b>"
        "{% endif %}"
    ),
    ScrollingGroup(
        Select(
            Jinja("{{ item.name }}"),
            item_id_getter=operator.attrgetter("id"),
            items="all",
            id="all",
            on_click=show_one,
            type_factory=int
        ),
        width=1,
        height=5,
        id="all_container",
        hide_on_single_page=True,
    ),
    Row(
        NextDialog(
            Jinja("➕ Добавить канал"),
            state=SubscriptionDutyForm.channel_info
        ),
        Button(
            Jinja(
                "{% if is_on %}"
                "❌ Выключить функцию"
                "{% else %}"
                "✅ Включить функцию"
                "{% endif %}"
            ),
            id="switch",
            on_click=switch_duty_state
        )
    ),
    PrevDialog(Jinja("⏪ Назад")),
    state=SubscriptionDutyDialog.root,
    getter=root_getter
)


get_channel_id = Window(
    Jinja(
        "<b>❗ Перед отправкой id канала боту убедитесь, что выполнили следующее условие:</b>\n\n"
        "<code>❗ Бот должен быть админом канала</code>"
    ),
    TextInput(
        id="channel_info",
        type_factory=int,
        on_success=on_channel_info_input
    ),
    SwitchToRoot(),
    state=SubscriptionDutyDialog.get_channel_id,
)

one_view = Window(
    Jinja(
        "<b>📢 Название: <code>{{ one.name }}</code></b>\n"
        "<b>♦ ID: <code>{{ one.id }}</code></b>\n\n"
        "<b>📎 Пригласительная ссылка:\n{{ one.invite_link }}</b>"
    ),
    Url(
        Jinja("👁 Перейти в канал"),
        url=Jinja("{{ one.invite_link }}")
    ),
    Row(
        Button(
            Jinja("🔄 Обновить ссылку"),
            id="update_invite_link",
            on_click=update_invite_link
        ),
        SwitchTo(
            Jinja("🗑 Удалить канал"),
            id="suggest_delete_one",
            state=SubscriptionDutyDialog.one_deletion
        )
    ),
    SwitchToRoot(Jinja("⏪ Назад")),
    state=SubscriptionDutyDialog.one_view,
    getter=DialogDataGetter("one"),
    disable_web_page_preview=True
)


one_deletion = Window(
    Jinja("<b>❓ Вы уверены, что хотите удалить канал из списка</b>"),
    Row(
        Button(
            Jinja("✅ Да"),
            id="submit_one_deletion",
            on_click=delete_one
        ),
        SwitchTo(
            Jinja("❌ Нет"),
            id="refuse_one_deletion",
            state=SubscriptionDutyDialog.one_view
        )
    ),
    state=SubscriptionDutyDialog.one_deletion,
    getter=DialogDataGetter("one_view")
)

check = Window(
    Jinja("<b>❗ Пока вы не подписались на следующие каналы, вы не сможете воспользоваться ботом</b>"),
    ListGroup(
        Url(
            text=Jinja("{{ item.name }}"),
            url=Jinja("{{ item.invite_link }}")
        ),
        items="unsubscribed_all",
        item_id_getter=operator.attrgetter("id"),
        id="unsubscribed_all_container",
    ),
    Button(
        Jinja("✅ Я подписался"),
        id="subscripted",
        on_click=complete_duty
    ),
    state=SubscriptionDutyDialog.check,
    getter=request_subscribe_getter
)


ui = Dialog(
    root,
    get_channel_id,
    one_view,
    one_deletion,
    check
)

uis = (
    ui,
    *forms
)

__all__ = (
    "uis",
)