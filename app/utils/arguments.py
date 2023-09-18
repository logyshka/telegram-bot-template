import argparse

from app.utils.misc import use_backup, prepare_first_start


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument(
        "--backup", "-b", type=str, help="path to backup.zip", default=None
    )
    parser.add_argument(
        "--first", "-f", action="store_true", help="start bot first_time"
    )
    return parser.parse_args()


async def use_arguments() -> None:
    arguments = parse_arguments()
    if arguments.backup:
        await use_backup(arguments.backup)
    if arguments.first:
        prepare_first_start()


__all__ = (
    "use_arguments",
)
