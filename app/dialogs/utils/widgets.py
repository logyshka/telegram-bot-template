import operator
from typing import Optional, TypeVar, Generic, Callable, Any, Union, Sequence

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode, Window
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup, Keyboard
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.kbd.select import ItemIdGetter
from aiogram_dialog.widgets.text import Text


class NextDialog(Button):

    def __init__(
            self,
            text: Text,
            state: State,
            start_mode: StartMode = StartMode.RESET_STACK,
            show_mode: ShowMode = ShowMode.EDIT,
            start_data: dict = None,
            on_click: Optional[OnClick] = None,
            save_prev: bool = True,
            when: WhenCondition = None,
    ):
        super().__init__(
            text=text,
            on_click=self._on_click,
            id=str(id(self)),
            when=when,
        )
        self.text = text
        self.show_mode = show_mode
        self.start_mode = start_mode
        self.state = state
        self.user_on_click = on_click
        self.start_data = start_data
        self.save_prev = save_prev

    async def _on_click(
            self,
            callback: CallbackQuery,
            button: Button,
            manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)

        await self.open(
            manager=manager,
            state=self.state,
            start_data=self.start_data,
            show_mode=self.show_mode,
            start_mode=self.start_mode,
            save_prev=self.save_prev
        )

    @classmethod
    async def open(
            cls,
            manager: DialogManager,
            state: State,
            start_data: dict = None,
            start_mode: StartMode = StartMode.RESET_STACK,
            show_mode: ShowMode = ShowMode.EDIT,
            save_prev: bool = True
    ):
        if start_data is None:
            start_data = {}

        if save_prev:
            start_data["prev_dialog"] = dict(
                state=manager.current_context().state,
                data=manager.start_data
            )

        await manager.done()
        await manager.start(
            state=state,
            data=start_data,
            mode=start_mode,
            show_mode=show_mode
        )


class PrevDialog(Button):

    def __init__(
            self,
            text: Text,
            start_mode: StartMode = StartMode.RESET_STACK,
            show_mode: ShowMode = ShowMode.EDIT,
            on_click: Optional[OnClick] = None,
            when: WhenCondition = None,
    ):
        super().__init__(
            text=text,
            on_click=self._on_click,
            id="__prev_dialog__",
            when=when,
        )
        self.text = text
        self.show_mode = show_mode
        self.start_mode = start_mode
        self.user_on_click = on_click

    async def _on_click(
            self,
            callback: CallbackQuery,
            button: Button,
            manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)

        await self.open(
            manager=manager,
            show_mode=self.show_mode,
            start_mode=self.start_mode
        )

    @classmethod
    async def open(
            cls,
            manager: DialogManager,
            start_mode: StartMode = StartMode.RESET_STACK,
            show_mode: ShowMode = ShowMode.EDIT
    ):
        prev_dialog_data = manager.start_data.get("prev_dialog")

        await manager.done()

        if prev_dialog_data:
            await manager.start(
                **prev_dialog_data,
                mode=start_mode,
                show_mode=show_mode
            )
