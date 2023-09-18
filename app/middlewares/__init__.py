from aiogram import Dispatcher

from app.data.config import Config


def register_middlewares(dispatcher: Dispatcher, config: Config):
    from . import throttling

    throttling.register_middleware(dp=dispatcher, config=config)


__all__ = (
    "register_middlewares",
)
