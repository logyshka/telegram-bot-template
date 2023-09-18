import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters import AdminFilter


router = Router()


@router.message(AdminFilter(), Command("ping"))
async def ping_handler(msg: Message):
    start = time.perf_counter_ns()
    reply_message = await msg.answer(
        "<code>⏱ Проверка пинга...</code>"
    )
    end = time.perf_counter_ns()
    ping = (end - start) * 0.000001
    await reply_message.edit_text(
        f"<b>⏱ Пинг: <code>{round(ping, 3)} ms</code></b>"
    )
