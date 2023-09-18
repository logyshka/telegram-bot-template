import logging

from aiogram import Router


def get_routers() -> list[Router]:
    from . import start

    routers = (
        start.router,
    )

    logging.info("User routers included")

    return routers
