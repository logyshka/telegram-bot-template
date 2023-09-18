import json
import pickle
from datetime import date

from aiogram.types import Message
from tortoise.fields import *
from tortoise.models import Model

from .enums import *


class User(Model):
    # Telegram user id
    id = IntField(pk=True)
    # Telegram username
    username = CharField(max_length=32, null=True)
    # User role
    role = CharEnumField(UserRole)
    # Is banned
    is_banned = BooleanField(default=False)
    # Creation date
    created_at = DateField(default=date.today())


class MailingLog(Model):
    # Database ID
    id = IntField(pk=True)
    # Total scope
    scope_all = IntField(default=0)
    # Succeed scope
    scope_succeed = IntField(default=0)
    # Failed scope
    scope_failed = IntField(default=0)
    # Duration
    duration = FloatField(null=True)


class PlannedMailing(Model):
    # Database ID
    id = IntField(pk=True)
    # Message for mailing
    message = JSONField(
        encoder=lambda value: value.json(),
        decoder=lambda value: Message(**json.loads(value))
    )
    # Scope database query
    scope = JSONField(
        encoder=lambda value: pickle.dumps(value),
        decoder=lambda value: pickle.loads(value)
    )
    # Start time
    run_date = DatetimeField()
    # Initiator id
    initiator_id = IntField()


class SubscriptionDuty(Model):
    # Telegram channel ID
    id = IntField(pk=True)
    # Telegram channel name
    name = CharField(max_length=255)
    # Actual invite link to the channel
    invite_link = CharField(max_length=255)


class SearchBookmark(Model):
    # Database id
    id = IntField(pk=True)
    # Section were searched
    section = CharEnumField(SearchSection)
    # Database id of searched item
    item_id = IntField()


__all__ = (
    "User",
    "MailingLog",
    "PlannedMailing",
    "SubscriptionDuty",
    "SearchBookmark"
)
