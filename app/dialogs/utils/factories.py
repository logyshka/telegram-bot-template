def time_factory(value: str) -> tuple[int, int]:
    if ":" not in value:
        raise ValueError()
    hours, minutes = value.split(":")

    try:
        hours = int(hours)

        if hours < 0 or hours > 24:
            raise ValueError()

        minutes = int(minutes)

        if minutes < 0 or minutes > 60:
            raise ValueError()

        return hours, minutes
    except:
        raise ValueError()


__all__ = (
    "time_factory",
)
