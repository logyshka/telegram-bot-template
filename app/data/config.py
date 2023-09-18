import logging
from typing import *

import toml

from pathlib import Path

from dataclasses import dataclass, asdict, fields, MISSING


class Storable:
    __path: Path
    __entity_to_save: "Storable" = None
    __loaded: bool = False

    def __setattr__(self, key, value) -> None:
        self.__dict__[key] = value

        if self.__loaded:
            self.__save()

    def __save(self) -> None:
        # noinspection PyDataclass
        dict_data = asdict(self.__entity_to_save)

        with open(self.__path, "w") as f:
            toml.dump(dict_data, f)

    @classmethod
    def configure_path(cls, path: Path) -> None:
        cls.__path = path

    @classmethod
    def make_loaded(cls, entity_to_save: "Storable") -> None:
        cls.__loaded = True
        cls.__entity_to_save = entity_to_save


@dataclass
class ConfigBot(Storable):
    token: str
    owner_id: int
    admin_ids: list[int]


@dataclass
class ConfigDatabase(Storable):
    models: list[str]
    protocol: str
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[str]

    def get_tortoise_config(self, database_path: str) -> dict:
        if self.protocol == "sqlite":
            db_url = f"{self.protocol}://{database_path}"
        else:
            db_url = f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}"

        return {
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": self.models,
                    "default_connection": "default",
                },
            },
        }


@dataclass
class ConfigMisc(Storable):
    throttling_rate: float
    backup_interval: int
    need_required_sub: bool


@dataclass
class Config(Storable):
    bot: ConfigBot
    misc: ConfigMisc
    database: ConfigDatabase


def parse_config(config_file: Path) -> Config:
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    Storable.configure_path(config_file)

    with open(config_file, "r") as f:
        data = toml.load(f)

    sections = {}

    for section in fields(Config):
        pre = {}

        current = data[section.name]

        for field in fields(section.type):
            if field.name in current:
                pre[field.name] = current[field.name]
            elif field.default is not MISSING:
                pre[field.name] = field.default
            else:
                raise ValueError(
                    f"Missing field {field.name} in section {section.name}"
                )

        sections[section.name] = section.type(**pre)

    config = Config(**sections)

    Storable.make_loaded(config)

    logging.info(f"Config was successfully parsed")

    return config


__all__ = (
    "parse_config",
    "Config",
)
