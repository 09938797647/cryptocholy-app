from core.bot import bot
from core.services.db import DBService
from core.settings import Config


if __name__ == "__main__":
    DBService.create_tables()
    if Config.WEBHOOK_URL:
        bot.run_webhook()
    else:
        bot.start_polling()
