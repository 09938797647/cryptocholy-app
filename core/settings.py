import os
from pathlib import Path

from core.constants import (
    DEFAULT_WRITE_MAX_RATE_PER_SECOND,
    DEFAULT_OVERALL_WRITE_MAX_RATE_PER_SECOND,
)

DEFAULT_API_BASE_URL = "https://api.telegram.org/bot"


class Config:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_USERNAME = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_QUEUE_NAME = os.getenv("REDIS_QUEUE_NAME")
    REDIS_SSL_ENABLED = bool(os.getenv("REDIS_SSL_ENABLED"))

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

    MYSQL_CONNECTION_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv(
        "TELEGRAM_BOT_USERNAME", "not_testing_with_bugs_guide_bot"
    )
    TELEGRAM_API_BASE_URL = os.getenv("TELEGRAM_API_BASE_URL", DEFAULT_API_BASE_URL)

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY")
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
    WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT") or 433)

    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")

    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    ADMIN_IDS = [
        int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(" ") if admin_id
    ]

    DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID")
    DEFAULT_LANGUAGE = "en"
    LANGUAGES = ["en", "ru", "be", "uk", "pl", "uz", "fa"]

    LIGHT_MODE = bool(os.getenv("LIGHT_MODE") or 0)
    ENABLE_CALLBACK_REPLIES = bool(os.getenv("ENABLE_CALLBACK_REPLIES") or 0)
    DISABLE_PS_BUTTON = bool(os.getenv("DISABLE_PS_BUTTON") or 0)
    IS_ACTIVE = bool(os.getenv("IS_ACTIVE") or 0)

    WRITE_MAX_RATE_PER_SECOND = int(
        os.getenv("WRITE_MAX_RATE_PER_SECOND") or DEFAULT_WRITE_MAX_RATE_PER_SECOND
    )
    OVERALL_WRITE_MAX_RATE_PER_SECOND = int(
        os.getenv("OVERALL_WRITE_MAX_RATE_PER_SECOND")
        or DEFAULT_OVERALL_WRITE_MAX_RATE_PER_SECOND
    )

    DEFAULT_QUEUE_BATCH_PROCESS_LIMIT = int(
        os.getenv("DEFAULT_QUEUE_BATCH_PROCESS_LIMIT") or 60
    )
    CONCURRENT_UPDATES = int(os.getenv("CONCURRENT_UPDATES") or 256)
    CONNECTION_POOL_SIZE = int(os.getenv("CONNECTION_POOL_SIZE") or 256)

    ROOT_PATH = Path("/app")
    STATIC_ROOT_PATH = ROOT_PATH / "static"
    STATIC_UPLOAD_PATH = STATIC_ROOT_PATH / "upload"

    API_TOKEN = os.getenv("API_TOKEN")
