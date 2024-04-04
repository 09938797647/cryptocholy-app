import hashlib
import hmac
import json
import os
from urllib.parse import unquote_plus

from fastapi import Header, HTTPException

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def validate_user_init_data(
    authorization_data: str = Header(..., alias="Authorization"),
) -> dict:
    c_str = "WebAppData"
    method, init_data = authorization_data.split(" ", 1)

    init_data = dict(
        sorted(
            [chunk.split("=") for chunk in init_data.split("&")],
            key=lambda x: x[0],
        )
    )

    _hash = init_data.pop("hash")

    # URL-decode the values
    init_data = {key: unquote_plus(value) for key, value in init_data.items()}

    # Generate the data_check_string
    data_check_string = "\n".join(
        [f"{key}={value}" for key, value in init_data.items()]
    )

    secret_key = hmac.new(
        c_str.encode(), TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256
    ).digest()
    data_check = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)

    if data_check.hexdigest() != _hash:
        raise HTTPException(status_code=400, detail="Invalid user data: wrong hash")

    user_data = json.loads(init_data.get("user", "{}"))
    user_data.pop("allows_write_to_pm", None)

    return user_data
