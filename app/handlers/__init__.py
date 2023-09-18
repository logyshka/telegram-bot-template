from aiogram import Dispatcher


def register_handlers(dispatcher: Dispatcher):
    from . import tech, owner, user, admin
    dispatcher.include_routers(
        tech.router,
        *owner.get_routers(),
        *user.get_routers(),
        *admin.get_routers()
    )
