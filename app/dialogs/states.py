from aiogram.fsm.state import State, StatesGroup


class UserDialog(StatesGroup):
    root = State()


class BackupDialog(StatesGroup):
    menu_view = State()
    get_file = State()
    confirmation = State()


class BackupForm(StatesGroup):
    file = State()
    confirmation = State()


class MailingDialog(StatesGroup):
    menu_view = State()
    planned_all_view = State()
    planned_one_view = State()
    planned_cancel = State()


class MailingForm(StatesGroup):
    message = State()
    scope = State()
    date = State()
    time = State()
    confirmation = State()


class SubscriptionDutyDialog(StatesGroup):
    root = State()
    get_channel_id = State()
    one_view = State()
    one_deletion = State()
    check = State()


class SubscriptionDutyForm(StatesGroup):
    channel_info = State()
    confirmation = State()


class SearchDialog(StatesGroup):
    menu_view = State()
    search = State()
    bookmarks = State()


class SearchUserDialog(StatesGroup):
    user_id = State()
    user_view = State()


class StatisticsDialog(StatesGroup):
    menu_view = State()
    user = State()
    mailing = State()


class AdminDialog(StatesGroup):
    menu_view = State()


class TestDialog(StatesGroup):
    root = State()


class CryptoPayDialog(StatesGroup):
    cash_out = State()
    cash_in = State()


__all__ = (
    "UserDialog",
    "BackupDialog",
    "BackupForm",
    "MailingDialog",
    "MailingForm",
    "SubscriptionDutyDialog",
    "SubscriptionDutyForm",
    "SearchDialog",
    "SearchUserDialog",
    "StatisticsDialog",
    "AdminDialog",
    "TestDialog",
    "CryptoPayDialog"
)
