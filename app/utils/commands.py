from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.data.config import Config

users_commands = {
    "start": "Запустить бота",
}

admin_commands = {
    **users_commands,
    "ping": "Проверить пинг бота",
    "admin": "Открыть админ-панель"
}

owner_commands = {
    **admin_commands,
}


async def setup_bot_commands(bot: Bot, config: Config):
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in owner_commands.items()
        ],
        scope=BotCommandScopeChat(chat_id=config.bot.owner_id),
    )
    for admin_id in config.bot.admin_ids:
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in admin_commands.items()
            ],
            scope=BotCommandScopeChat(chat_id=admin_id),
        )
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_bot_commands(bot: Bot, config: Config):
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    for admin_id in config.bot.admin_ids:
        await bot.delete_my_commands(
            scope=BotCommandScopeChat(chat_id=admin_id),
        )
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=config.bot.owner_id)
    )

__all__ = (
    "setup_bot_commands",
    "remove_bot_commands"
)
