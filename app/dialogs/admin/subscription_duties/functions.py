from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import *
from aiogram_dialog.widgets.kbd import *

from app.dialogs.states import SubscriptionDutyDialog, UserDialog, SubscriptionDutyForm
from app.dialogs.utils.widgets import NextDialog
from app.services.database import SubscriptionDuty


async def on_channel_info_input(msg: Message, widget: MessageInput, manager: DialogManager):
    bot = manager.middleware_data["bot"]
    if msg.forward_from_chat:
        channel_id = msg.forward_from_chat.id
    else:
        channel_id = msg.text if msg.text else "error"

    try:
        duty = await SubscriptionDuty.can_create_one(
            channel_id=int(channel_id),
            bot=bot
        )
        if duty:
            manager.dialog_data["duty"] = duty
            await manager.switch_to(SubscriptionDutyForm.confirmation)
            return
        else:
            error = "канал с данным id уже добавлен"
    except ValueError:
        error = "некорректный id"
    except Exception:
        error = "бот не является админом канала"

    manager.dialog_data["error"] = error


async def create_duty(call: CallbackQuery, widget: Button, manager: DialogManager):
    duty = manager.dialog_data["duty"]
    await duty.save()
    await call.answer("✅ Канал успешно добавлен!")


async def show_one(call: CallbackQuery, widget: Button, manager: DialogManager, channel_id: int):
    bot = manager.middleware_data["bot"]
    manager.dialog_data["one"] = await SubscriptionDuty.get_one(
        channel_id=channel_id,
        bot=bot
    )
    await manager.switch_to(SubscriptionDutyDialog.one_view)


async def update_invite_link(call: CallbackQuery, widget: Button, manager: DialogManager):
    one = manager.dialog_data["one"]
    bot = manager.middleware_data["bot"]
    ok = await one.update_invite_link(bot=bot)

    if ok:
        await manager.update({"one": one})
    else:
        await manager.switch_to(SubscriptionDutyDialog.root)


async def delete_one(call: CallbackQuery, widget: Button, manager: DialogManager):
    one = manager.dialog_data["one"]

    await one.delete()
    await call.answer("✅ Канал успешно удалён!")
    await manager.switch_to(SubscriptionDutyDialog.root)


async def switch_duty_state(call: CallbackQuery, widget: Button, manager: DialogManager):
    config = manager.middleware_data["config"]
    config.misc.need_required_sub = not config.misc.need_required_sub
    await manager.update({"is_on": config.misc.need_required_sub})


async def complete_duty(call: CallbackQuery, widget: Button, manager: DialogManager):
    bot = manager.middleware_data["bot"]
    unsubscribed_all = await SubscriptionDuty.get_unsubscribed_all(
        bot=bot,
        user_id=call.from_user.id
    )

    if len(unsubscribed_all) == 0:
        await NextDialog.open(
            manager=manager,
            state=UserDialog.root
        )
    else:
        await call.answer(
            "⚠ Вы всё ещё не подписаны на все каналы!",
            show_alert=True
        )
        await manager.update({
            "unsubscribed_all": unsubscribed_all
        })


__all__ = (
    "on_channel_info_input",
    "create_duty",
    "show_one",
    "update_invite_link",
    "delete_one",
    "switch_duty_state",
    "complete_duty",
)