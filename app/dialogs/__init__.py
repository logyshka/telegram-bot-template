from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs


def register_dialogs(dispatcher: Dispatcher):
    from . import user, admin, test

    dispatcher.include_routers(
        test.ui,
        *user.uis,
        *admin.uis,
    )

    setup_dialogs(dispatcher)
