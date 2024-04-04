import redis
from telegram import Update

from core.settings import Config

DEFAULT_EXPIRATION_SECONDS = 30
DEFAULT_FILE_ID_EXPIRATION_SECONDS = 60 * 55
DEFAULT_FILE_EXPIRATION_SECONDS = 60 * 30


redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    username=Config.REDIS_USERNAME,
    password=Config.REDIS_PASSWORD,
    ssl_check_hostname=False,
    ssl=Config.REDIS_SSL_ENABLED,
)


def format_file_cache_key(image_path: str) -> str:
    return f"image:{image_path}"


def format_bytes_cache_key(image_path: str) -> str:
    return f"bytes:{image_path}"


def set_file_id_cache(key: str, file_id: str) -> None:
    redis_client.setex(key, DEFAULT_FILE_ID_EXPIRATION_SECONDS, file_id)


def set_file_cache(key: str, file: bytes) -> None:
    redis_client.setex(key, DEFAULT_FILE_EXPIRATION_SECONDS, file)


def get_cache_value(key: str) -> str | None:
    value = get_cache_bytes_value(key)
    if value is not None:
        return value.decode("utf-8")  # noqa


def get_cache_bytes_value(key: str) -> bytes | None:
    return redis_client.get(key)


def format_response_cache_key_value(
    command: str, kwargs: dict
) -> tuple[str | None, bytes | None]:
    if not kwargs or not (chat_id := kwargs.get("chat_id")):
        return None, None

    return f"response:{chat_id}", f"{command}{kwargs}".encode("utf-8")


def format_request_cache_key_value(
    update: Update,
) -> tuple[str, bytes] | tuple[None, None]:
    if not update or not update.effective_chat.id:
        return None, None

    if update.callback_query:
        return f"callback:{update.effective_chat.id}", str(
            update.callback_query.data
        ).encode("utf-8")

    elif update.message and update.message.text:
        return f"message:{update.effective_chat.id}", str(update.message.text).encode(
            "utf-8"
        )

    return None, None


def add_user_action_cache(key: str, value: bytes):
    redis_client.setex(key, DEFAULT_EXPIRATION_SECONDS, value)


def check_user_action_cache(key: str, value: bytes) -> bool:
    return redis_client.getex(key) == value
