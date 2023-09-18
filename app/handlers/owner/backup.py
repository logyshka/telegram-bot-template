from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dialogs.states import BackupDialog
from app.filters import OwnerFilter
from app.services.database import User


router = Router()


@router.message(OwnerFilter(), Command("from_backup"))
async def start(msg: Message, dialog_manager: DialogManager, user: User):
    await dialog_manager.start(
        state=BackupDialog.get_file,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )
