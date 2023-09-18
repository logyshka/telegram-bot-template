import logging
import os
import pathlib
import platform
import shutil
import sys
import zipfile
from typing import *

from app.data.config import parse_config
from app.data.const import *


def clean_from_html(text: str) -> str:
    data = ""
    is_open = False
    for i in str(text):
        if is_open and i == ">":
            is_open = False
        elif i == "<":
            is_open = True
        elif not is_open:
            data += i
    return data


def get_path_instance() -> pathlib.Path:
    Path = pathlib.WindowsPath if sys.platform.startswith("win") else pathlib.PosixPath
    pathlib.WindowsPath = Path
    pathlib.PosixPath = Path
    return Path


async def use_backup(backup_path: str) -> None:
    backup_file = pathlib.Path(backup_path).resolve()
    if backup_file.exists():
        try:
            backup = zipfile.ZipFile(
                file=backup_file,
                mode="r"
            )
            backup.extract(CONFIG_FILE.name, BACKUP_DIR)
            backup.extract(DATABASE_FILE.name, BACKUP_DIR)

            parse_config(CONFIG_BACKUP_FILE)

            shutil.copyfile(DATABASE_BACKUP_FILE, DATABASE_FILE)
            shutil.copyfile(CONFIG_BACKUP_FILE, CONFIG_FILE)
        except Exception:
            raise TypeError(f"{backup_file} is incorrect file!")
    else:
        raise FileNotFoundError(f"{backup_file} is not exists!")


def prepare_first_start() -> None:
    remove_files_from_dir(STORAGE_DIR, STATIC_DIR)


def remove_files_from_dir(path: pathlib.Path, *exceptions: str) -> None:
    for entry in os.scandir(path):
        path = pathlib.Path(entry.path)
        if entry.is_file():
            path.unlink()
        elif entry.is_dir() and path not in exceptions:
            remove_files_from_dir(path, *exceptions)


async def ignore_async(*functions: Coroutine, show_log: bool = False):
    for function_ in functions:
        try:
            await function_
        except Exception as e:
            if show_log:
                logging.exception(e)


def get_file_creation_date(path_to_file):
    if platform.system() == 'Windows':
        try:
            return os.path.getctime(path_to_file)
        except Exception:
            return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
