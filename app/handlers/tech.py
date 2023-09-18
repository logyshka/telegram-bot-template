from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.types import Message, CallbackQuery, ErrorEvent
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from app.dialogs.states import SubscriptionDutyDialog, TestDialog, UserDialog
from app.filters import SubscriptionFilter, AdminFilter

router = Router()

not_subscripted_filters = (~SubscriptionFilter(), ~AdminFilter())


@router.message(*not_subscripted_filters)
async def not_subscripted_handler(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=SubscriptionDutyDialog.check,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


@router.callback_query(*not_subscripted_filters)
async def not_subscripted_handler(_call: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=SubscriptionDutyDialog.check,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


@router.errors(ExceptionTypeFilter(UnknownIntent, UnknownState))
async def unknown_intent_handler(error: ErrorEvent, dialog_manager: DialogManager):
    call = error.update.callback_query
    try:
        await call.message.delete()
        await dialog_manager.start(
            state=UserDialog.root,
            show_mode=ShowMode.EDIT,
            mode=StartMode.RESET_STACK
        )
    except:
        await call.answer("❗ Данный диалог недействителен")


@router.message(Command("test"))
async def test_handler(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=TestDialog.root,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        data={"test": 1}
    )
