from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from core.services.db import DBService
from core.services.user import UserService


def require_user_account(f):
    @wraps(f)
    def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        with DBService().db_session() as db_session:
            user_service = UserService(db_session)
            user_service.get_or_create(telegram_user=update.effective_user)

        return f(update, context)

    return inner
