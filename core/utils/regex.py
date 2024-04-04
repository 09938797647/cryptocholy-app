import re


def get_id_from_callback(
    callback_data: str | None, regex: re.Pattern, id_key: str = "id"
) -> int | None:
    if callback_data is None:
        return None

    match = regex.match(callback_data)
    if match:
        return match.groupdict()[id_key]

    return None
