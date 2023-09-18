from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dialogs.states import AdminDialog


router = Router()


@router.message(Command("admin"))
async def panel_handler(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=AdminDialog.menu_view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )

