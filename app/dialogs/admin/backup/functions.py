from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from app.data.const import BACKUP_SUMMARY_FILE
from app.services import events
from app.utils.misc import use_backup, clean_from_html


async def make_backup(call: CallbackQuery, _: Button, manager: DialogManager):
    await events.interval.make_backup(
        bot=manager.middleware_data["bot"],
        config=manager.middleware_data["config"]
    )


async def on_file_input(msg: Message, _: MessageInput, manager: DialogManager):
    bot = manager.middleware_data["bot"]
    file_id = msg.document.file_id
    await bot.download(
        file=file_id,
        destination=BACKUP_SUMMARY_FILE
    )
    await manager.next()


async def on_accept_input(call: CallbackQuery, widget: Button, manager: DialogManager):
    try:
        await use_backup(BACKUP_SUMMARY_FILE)
        await call.answer("✅ Бэкап успешно использован!")
    except Exception as error:
        await call.answer(f"⚠ Ошибка: {clean_from_html(str(error))}", True)


__all__ = (
    "on_file_input",
    "on_accept_input",
    "make_backup",
)
