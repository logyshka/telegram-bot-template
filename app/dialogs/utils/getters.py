import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any, Union, Callable, Awaitable, Dict

from aiogram_dialog import DialogManager


@dataclass
class GetterField:
    name: str
    result_name: Optional[str] = None
    default_value: Optional[Any] = None


class Getter(ABC):
    @abstractmethod
    async def __call__(self, **kwargs) -> dict:
        pass


class DialogManagerDataGetter(Getter):
    def __init__(self, section_name: str, *fields: Union[str, GetterField]) -> None:
        self.fields = []

        for field in fields:
            if isinstance(field, GetterField):
                self.fields.append(field)
            elif isinstance(field, str):
                self.fields.append(GetterField(name=field))

        self.section_name = section_name

    async def __call__(self, dialog_manager: DialogManager, **kwargs) -> dict:
        data = {}

        section = operator.attrgetter(self.section_name)(dialog_manager)

        for field in self.fields:
            data[field.result_name or field.name] = section.get(field.name) or field.default_value

        return data


class DialogDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("dialog_data", *fields)


class StartDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("start_data", *fields)


class MiddlewareDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("middleware_data", *fields)


class StaticDataGetter(Getter):

    def __init__(self, **values: Any) -> None:
        self.values = values

    async def __call__(self, **kwargs) -> dict:
        return self.values


class AsyncStaticDataGetter(Getter):

    def __init__(self, **values: Any) -> None:
        self.values = values

    async def __call__(self, **kwargs) -> dict:
        for key in self.values.keys():
            value = self.values[key]
            if isinstance(value, Callable):
                self.values[key] = await value()
            else:
                self.values[key] = await value


class UnionGetter(Getter):
    def __init__(self, *getters: Union[Getter, Callable[..., Awaitable[Dict]]]):
        self._getters = getters

    async def __call__(self, **kwargs):
        result = {}

        for getter in self._getters:
            getter_data = await getter(**kwargs)
            for key in getter_data:
                if not result.get(key):
                    result[key] = getter_data[key]
        return result


__all__ = (
    "Getter",
    "DialogDataGetter",
    "StartDataGetter",
    "MiddlewareDataGetter",
    "StaticDataGetter",
    "AsyncStaticDataGetter",
    "UnionGetter",
    "GetterField",
)
