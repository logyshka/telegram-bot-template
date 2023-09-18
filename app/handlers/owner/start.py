from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from app.dialogs.states import UserDialog
from app.filters import OwnerFilter
from app.services.database import User

router = Router()
owner_filter = OwnerFilter()
router.message.filter(owner_filter)
router.callback_query.filter(owner_filter)


@router.message(Command("start"))
async def start(msg: Message, dialog_manager: DialogManager, user: User):
    await user.update(username=msg.from_user.id)
    await dialog_manager.start(
        state=UserDialog.root,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )
