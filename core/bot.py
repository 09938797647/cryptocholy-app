import logging
from warnings import filterwarnings

from telegram.warnings import PTBUserWarning

from core.constants import POOL_TIMEOUT
from telegram.ext import (
    ApplicationBuilder,
    Application,
)

from core.not_telegram_ext.limiter import NotAIORateLimiter
from core.not_telegram_ext.processor import MyUpdateProcessor
from core.settings import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)


class NotBot:
    def __init__(self, token: str) -> None:
        self.__token = token
        rate_limiter = NotAIORateLimiter(
            write_max_rate=Config.WRITE_MAX_RATE_PER_SECOND,
            write_time_period=1,
            overall_max_rate=Config.OVERALL_WRITE_MAX_RATE_PER_SECOND,
            overall_time_period=1,
            # max_retries=1,
        )
        self.application: Application = (
            ApplicationBuilder()
            .pool_timeout(POOL_TIMEOUT)
            .base_url(base_url=Config.TELEGRAM_API_BASE_URL)
            .token(token)
            .concurrent_updates(MyUpdateProcessor(Config.CONCURRENT_UPDATES))
            .connection_pool_size(Config.CONNECTION_POOL_SIZE)
            .rate_limiter(rate_limiter)
            .build()
        )
        self.configure_handlers()
        self.configure_tasks()

    def configure_handlers(self):
        self.application.add_handlers([])

    def configure_tasks(self):
        pass

    def start_polling(self):
        logger.info("Start polling")
        self.application.run_polling()

    def run_webhook(self):
        self.application.run_webhook(
            listen=Config.WEBHOOK_HOST,
            port=Config.WEBHOOK_PORT,
            url_path=Config.TELEGRAM_BOT_TOKEN,
            secret_token=Config.WEBHOOK_SECRET_KEY,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.TELEGRAM_BOT_TOKEN}",
            max_connections=100,
        )


bot = NotBot(token=Config.TELEGRAM_BOT_TOKEN)
