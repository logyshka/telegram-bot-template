from pathlib import Path

from aiogram.enums import ParseMode
from pytz import utc

ROOT_DIR = Path(__file__).parent.parent.parent
APP_DIR = ROOT_DIR / "app"
STORAGE_DIR = APP_DIR / "data" / "storage"
STATIC_DIR = STORAGE_DIR / "static"
BACKUP_DIR = STORAGE_DIR / "backup"
BACKUP_SUMMARY_FILE = BACKUP_DIR / "backup.zip"

CONFIG_FILE = ROOT_DIR / "config.toml"
CONFIG_BACKUP_FILE = BACKUP_DIR / CONFIG_FILE.name

DATABASE_DIR = STORAGE_DIR / "database"
MIGRATION_DIR = DATABASE_DIR / "migrations"
DATABASE_FILE = DATABASE_DIR / "database.sqlite"
DATABASE_BACKUP_FILE = BACKUP_DIR / DATABASE_FILE.name

STATISTICS_DIR = STORAGE_DIR / "statistics"
TEMPLATES_DIR = APP_DIR / "templates"

BOT_PARSE_MODE = ParseMode.HTML
TZ_INFO = utc

__all__ = (
    "BACKUP_DIR",
    "BACKUP_SUMMARY_FILE",
    "CONFIG_FILE",
    "CONFIG_BACKUP_FILE",
    "STORAGE_DIR",
    "DATABASE_DIR",
    "MIGRATION_DIR",
    "DATABASE_FILE",
    "DATABASE_BACKUP_FILE",
    "BOT_PARSE_MODE",
    "STATIC_DIR",
    "TZ_INFO",
    "STATISTICS_DIR",
    "TEMPLATES_DIR",
)
