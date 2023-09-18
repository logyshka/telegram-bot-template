import logging
from datetime import datetime

from aiogram import Bot
from aiogram.types import ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from tortoise.expressions import *
from tortoise.functions import *
from tortoise.queryset import QuerySet, ExistsQuery

from .enums import *
from .models import *
from ...data.config import Config
from ...data.const import TZ_INFO


class User(User):
    @classmethod
    async def register(
            cls,
            config: Config,
            user_id: int,
            username: str
    ) -> "User":
        user = await cls.get_or_none(id=user_id)

        if user:
            return user

        if user_id == config.bot.owner_id:
            role = UserRole.OWNER
        elif user_id in config.bot.admin_ids:
            role = UserRole.ADMIN
        else:
            role = UserRole.USER

        return await cls.create(
            id=user_id,
            username=username,
            role=role
        )

    @classmethod
    async def create_static(
            cls,
            config: Config,
            bot: Bot
    ) -> None:
        for admin_id in [*config.bot.admin_ids, config.bot.owner_id]:
            try:
                chat = await bot.get_chat(admin_id)
                await cls.register(config, admin_id, chat.username)
            except Exception as e:
                logging.exception(e)
                logging.warning(
                    f"Admin with ID={admin_id} haven't started chat with bot yet! Ask him to do it or remove his ID from admin list!")
                logging.shutdown()
                exit(-1)

    @classmethod
    async def search_user(cls, user_id: Union[str, int]) -> Optional["User"]:
        try:
            if user_id[0] == "@":
                user = await User.get_or_none(username=user_id[1:])
            else:
                user = await User.get_or_none(id=user_id[1:])
            return user
        except Exception:
            return None

    @classmethod
    def get_all(cls) -> QuerySet["User"]:
        return cls.filter()

    @classmethod
    def get_admins(cls) -> QuerySet["User"]:
        return cls.filter(Q(role=UserRole.ADMIN) | Q(role=UserRole.OWNER))

    async def update(self, **kwargs) -> None:
        await self.filter(id=self.id).update(**kwargs)


class MailingLog(MailingLog):
    @classmethod
    async def get_count(cls) -> int:
        return await cls.filter().count()

    @classmethod
    async def get_average_duration(cls) -> str:
        total_duration = await cls.filter().annotate(total_duration=Sum("duration")).values("total_duration")
        total_duration = total_duration[0]["total_duration"]

        average_duration = (total_duration if total_duration else 0) / (await cls.get_count() or 1)
        return cls.format_duration(average_duration)

    @classmethod
    async def get_average_scope(cls) -> tuple[int, int, int]:
        mailings_count = await cls.get_count()
        result = (await cls.filter().annotate(
            all=Sum("scope_all"),
            succeed=Sum("scope_succeed"),
            failed=Sum("scope_failed")
        ).values())[0]

        result = tuple(
            result[key] // mailings_count if result[key] else 0 for key in ("all", "succeed", "failed")
        )
        return result

    @staticmethod
    def format_duration(duration: float):
        if duration < 60:
            return f"{duration} сек"
        elif duration < 3600:
            minutes = duration // 60
            seconds = duration % 60
            return f"{minutes}.{seconds} мин"
        hours = duration // 3600
        duration %= 3600
        minutes = duration // 60
        seconds = duration % 60
        return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"


class PlannedMailing(PlannedMailing):
    @classmethod
    async def get_all(cls) -> list["PlannedMailing"]:
        now = datetime.now(tz=TZ_INFO)
        await cls.filter(run_date__lt=now).delete()
        return await cls.filter()


class SubscriptionDuty(SubscriptionDuty):
    @classmethod
    async def get_all(cls, bot: Bot) -> list["SubscriptionDuty"]:
        items = await cls.filter()

        result = []

        for item in items:
            if await item.validate(bot=bot):
                result.append(item)

        return result

    @classmethod
    async def get_unsubscribed_all(cls, bot: Bot, user_id: int) -> list["SubscriptionDuty"]:
        channels = await SubscriptionDuty.get_all(bot=bot)
        result = []

        for channel in channels:
            if not await channel.is_user_member(
                    bot=bot,
                    user_id=user_id
            ):
                result.append(channel)

        return result

    @classmethod
    async def get_one(cls, channel_id: int, bot: Bot) -> Optional["SubscriptionDuty"]:
        item = await SubscriptionDuty.get_or_none(id=channel_id)

        if item:
            if await item.validate(bot=bot):
                return item
        return None

    @classmethod
    async def can_create_one(cls, channel_id: int, bot: Bot) -> Optional["SubscriptionDuty"]:
        invite_link = await bot.export_chat_invite_link(chat_id=channel_id)

        if await cls.exists(id=channel_id):
            return None

        name = (await bot.get_chat(chat_id=channel_id)).title

        return cls(
            id=channel_id,
            name=name,
            invite_link=invite_link
        )

    async def validate(self, bot: Bot) -> bool:
        try:
            await bot.get_chat(chat_id=self.id)
            return True
        except:
            await self.delete()
            return False

    async def update_invite_link(self, bot: Bot) -> bool:
        try:
            self.invite_link = await bot.export_chat_invite_link(chat_id=self.id)
            await self.save()
            return True
        except:
            await self.delete()
            return False

    async def is_user_member(self, bot: Bot, user_id: int) -> bool:
        try:
            member = await bot.get_chat_member(
                chat_id=self.id,
                user_id=user_id
            )
            return isinstance(member, (ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner))
        except Exception:
            await self.delete()
            return True


class SearchBookmark(SearchBookmark):
    @classmethod
    async def switch_user(cls, user_id: int) -> bool:
        kwargs = dict(
            item_id=user_id,
            section=SearchSection.USER
        )
        user = await cls.get_or_none(**kwargs)
        if user:
            await user.delete()
        else:
            user = await cls.create(**kwargs)
        return await user.exists()

    @classmethod
    def is_user_saved(cls, user_id: int) -> ExistsQuery:
        return cls.exists(
            item_id=user_id,
            section=SearchSection.USER
        )


__all__ = (
    "User",
    "MailingLog",
    "PlannedMailing",
    "SubscriptionDuty",
    "SearchBookmark"
)
