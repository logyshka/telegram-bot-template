from datetime import date, timedelta

import matplotlib.pyplot as plt
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import *

from app.data.const import STATISTICS_DIR
from app.services.database import User


async def get_user_income_week() -> tuple[str, int]:
    path = STATISTICS_DIR / "user_week_income.png"
    start_date = date.today()

    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    users_income = []

    day1 = timedelta(days=1)

    while start_date.weekday() != 0:
        start_date -= day1

    for _ in range(7):
        users_income.append(
            await User.filter(created_at=start_date).count()
        )
        start_date += day1

    plt.figure(figsize=(9, 6))
    plt.bar(weekdays, users_income)
    plt.title("Новых пользователей за текущую неделю")
    plt.xlabel("День недели")
    plt.ylabel("Кол-во пользователей")

    plt.savefig(path)
    return path, sum(users_income)


async def get_user_income_month() -> tuple[str, int]:
    path = STATISTICS_DIR / "user_month_income.png"

    today = date.today()
    day1 = timedelta(days=1)
    last_day = date(year=today.year, month=today.month, day=28)
    day = date(year=today.year, month=today.month, day=1)

    while last_day.month == today.month:
        last_day += day1

    last_day -= day1

    days = [f"{i:2d}" for i in range(1, last_day.day + 1)]
    users_income = []

    for i in range(last_day.day):
        users_income.append(await User.filter(created_at=day).count())
        day += day1

    plt.figure(figsize=(9, 6))
    plt.bar(days, users_income)
    plt.title("Новых пользователей за текущий месяц")
    plt.xlabel("День")
    plt.ylabel("Кол-во пользователей")

    plt.savefig(path)
    return path, sum(users_income)


async def switch_user_graphic(call: CallbackQuery, widget: Checkbox, manager: DialogManager) -> None:
    current_id = manager.dialog_data.get("current_id") or 0
    ids = ["user_income_week", "user_income_month"]
    current_id = (current_id + 1) % len(ids)
    manager.dialog_data["graphic_id"] = ids[current_id]
    manager.dialog_data["current_id"] = current_id
    widget.set_widget_data(manager, True)
