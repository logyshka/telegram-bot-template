from datetime import date, datetime

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Calendar, Select

from app.data.const import TZ_INFO
from app.dialogs.states import MailingDialog, MailingForm
from app.dialogs.utils.widgets import PrevDialog
from app.services.database import User
from app.services.events.once import mail, plan_mail, MailConfig


async def on_get_message(msg: Message, _: MessageInput, manager: DialogManager):
    if msg.forward_from:
        manager.dialog_data["mail_config"] = MailConfig(
            initiator_id=msg.from_user.id,
            bot=manager.middleware_data["bot"],
            message=msg
        )
        await manager.next()
    else:
        await msg.answer(
            "<b>⚠ Сообщение должно быть переслано!</b>"
        )


async def on_choice_scope(call: CallbackQuery, _: Button, manager: DialogManager):
    scopes = {
        "all_users": User.get_all(),
        "admins": User.get_admins(),
    }
    manager.dialog_data["mail_config"].scope = scopes[call.data]

    if manager.start_data["is_planning"]:
        await manager.next()
    else:
        await manager.switch_to(MailingForm.confirmation)


async def on_choice_date(call: CallbackQuery, _: Calendar, manager: DialogManager, date_: date):
    if date_ < date.today():
        await call.answer("⚠ Нельзя выбрать прошедшую дату!")
    else:
        manager.dialog_data["date"] = date_
        await manager.next()


async def on_time_input(msg: Message, _: TextInput, manager: DialogManager, time_: tuple[int, int]):
    date_ = manager.dialog_data["date"]

    run_date = datetime(
        year=date_.year,
        month=date_.month,
        day=date_.day,
        hour=time_[0],
        minute=time_[1],
        tzinfo=TZ_INFO
    )

    now = datetime.now(TZ_INFO)

    if run_date > now:
        manager.dialog_data["run_date"] = run_date
        await manager.next()
    else:
        await msg.answer("<b>⚠ Вы не можете выбрать время в прошлом!</b>")


async def create_one(call: CallbackQuery, _: Button, manager: DialogManager):
    dialog_data = manager.dialog_data.copy()
    is_planning = manager.start_data.get("is_planning")
    scheduler = manager.middleware_data["scheduler"]

    if is_planning:
        run_date = dialog_data["run_date"]
        job = await plan_mail(
            mail_config=dialog_data["mail_config"],
            run_date=run_date,
            scheduler=scheduler
        )
        await call.message.answer(
            f"<b>✅ Рассылка успешно запланирована на <code>{run_date}</code></b>\n"
            f"<b>🆔 ID рассылки: <code>{job.id}</code></b>"
        )
        await PrevDialog.open(manager=manager)
    else:
        await PrevDialog.open(manager=manager)
        await mail(mail_config=dialog_data["mail_config"])


async def mailing_preview(call: CallbackQuery, _: Button, manager: DialogManager):
    message = manager.dialog_data["mail_config"].message
    await call.message.answer(
        text="<b>✉ Вот сообщение, которое будет использоваться в рассылке: </b>"
    )
    await message.copy_to(
        chat_id=call.from_user.id,
        reply_markup=message.reply_markup
    )


async def show_planned_one(_call: CallbackQuery, _: Select, manager: DialogManager, job_id: str):
    job = manager.middleware_data["scheduler"].get_job(job_id=job_id)
    if job:
        manager.dialog_data["planned_one"] = job
        manager.dialog_data["mail_config"] = job.kwargs["mail_config"]
        await manager.switch_to(MailingDialog.planned_one_view)
    else:
        await manager.show()


async def cancel_planned(_call: CallbackQuery, _: Button, manager: DialogManager):
    job_id = manager.dialog_data["planned_one"].id
    scheduler = manager.middleware_data["scheduler"]
    job = scheduler.get_job(job_id=job_id)
    if job:
        job.remove()
    await manager.switch_to(MailingDialog.planned_all_view)


async def on_choice_type(call: CallbackQuery, _widget: Button, manager: DialogManager):
    is_planning = call.data == "plan"
    manager.dialog_data["is_planning"] = is_planning


__all__ = (
    "on_get_message",
    "on_choice_scope",
    "on_choice_type",
    "on_time_input",
    "on_choice_date",
    "create_one",
    "mailing_preview",
    "show_planned_one",
    "cancel_planned"
)
