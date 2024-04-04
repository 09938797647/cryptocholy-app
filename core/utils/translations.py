import functools
import gettext
from collections.abc import Callable

from telegram import Update
from telegram.ext import ContextTypes

from core.models.user import User
from core.settings import Config


def set_language(language: str | None) -> gettext.GNUTranslations:
    language = language if language in Config.LANGUAGES else Config.DEFAULT_LANGUAGE
    # Load translations
    locale = gettext.translation(
        "messages", localedir="translations", languages=[language]
    )
    # Install translations for the current session
    locale.install()
    return locale


def get_local_language_for_user(user: type[User]) -> Callable[[str], str]:
    locale = set_language(user.language)
    return locale.gettext


def translation_handler_wrapper(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Set translations for the current session
        language = update.effective_user.language_code
        locale = set_language(language=language)
        # Call the original function
        result = await func(update=update, context=context, _t=locale.gettext)

        return result

    return wrapper
