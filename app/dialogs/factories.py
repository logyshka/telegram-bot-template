import re


def cp_link_factory(value: str) -> str:
    match = re.search(r"https?://t\w?\.me/CryptoBot\?start=(\w+)", value)

    if not match:
        raise ValueError()

    return match.group(1)
