import logging

from aiogram import Router

from app.filters import OwnerFilter


def get_routers() -> list[Router]:
    routers = (

    )
    for router in routers:
        router.message.filter(OwnerFilter())
        router.callback_query.filter(OwnerFilter())

    logging.info("Owner routers included")

    return routers
