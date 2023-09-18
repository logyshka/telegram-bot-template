import json
import pickle

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from tortoise.functions import Sum

from app.data.config import Config
from app.dialogs.states import UserDialog
from app.services.database import User


router = Router()


@router.message(Command("start"))
async def start(msg: Message, dialog_manager: DialogManager, user: User, config: Config):
    if user is None:
        await User.register(
            config=config,
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )
    await dialog_manager.start(
        state=UserDialog.root,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )
