from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput


async def save_on_input(msg: Message, widget: TextInput, manager: DialogManager, data: Any):
    manager.dialog_data[widget.widget_id] = data
    await manager.next()


async def migrate_start_data(start_data: dict, manager: DialogManager):
    manager.dialog_data.update(**start_data)


__all__ = (
    "save_on_input",
    "migrate_start_data"
)
