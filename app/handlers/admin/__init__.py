import logging

from aiogram import Router

from app.filters import AdminFilter


def get_routers() -> list[Router]:
    from . import ping, panel
    routers = (
        ping.router,
        panel.router,
    )
    for router in routers:
        router.message.filter(AdminFilter())
        router.callback_query.filter(AdminFilter())

    logging.info("Admin routers included")

    return routers
