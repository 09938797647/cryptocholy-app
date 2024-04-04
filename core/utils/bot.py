import logging
import time
from functools import wraps
from pathlib import Path

from telegram import Update, InlineKeyboardMarkup, InputMediaPhoto, Message
from telegram._utils.types import FileInput
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from core.settings import Config
from core.utils.cache import format_file_cache_key, get_cache_value, set_file_id_cache

logger = logging.getLogger(__name__)


async def remove_previous_callbacks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    ...
    # await context.bot.edit_message_text(
    #     chat_id=update.effective_chat.id,
    #     message_id=update.effective_message.message_id,
    #     text=update.effective_message.text,
    # )


async def answer_callback_query(update: Update) -> None:
    if Config.ENABLE_CALLBACK_REPLIES and update.callback_query:
        try:
            start = time.time()
            await update.callback_query.answer()
            logger.info(
                "%s\tAnswered callback query to user `%d` in %.2f seconds",
                answer_callback_query.__name__,
                update.effective_chat.id,
                time.time() - start,
            )
        except BaseException as exc:
            # We can just ignore this if we're timing out on this request
            logger.debug("Can't answer callback query %s", exc)
            pass


def get_or_set_file_id(f):
    @wraps(f)
    async def inner(
        photo_path: str | Path | None = None,
        document: FileInput | None = None,
        **kwargs,
    ) -> None:
        if Config.LIGHT_MODE:
            result = await f(document=None, **kwargs)
            logger.info(
                "%s\tSent message to user `%d` in light mode",
                f.__name__,
                kwargs["chat_id"],
            )
            return result

        if not (document or photo_path):
            raise AttributeError("Either document of photo_path should be provided")

        media = document
        cache_key = format_file_cache_key(image_path=photo_path)
        if media is None:
            media = get_cache_value(cache_key)
            logger.debug("File ID from cache %s", media)
            if not media and photo_path:
                logger.debug("Reading from file")
                full_path = Config.STATIC_ROOT_PATH / photo_path
                if full_path.is_file():
                    with open(full_path, "rb") as file:
                        media = file.read()
                else:
                    logger.error(
                        "Can't read file %s. Falling back to text message", photo_path
                    )

        if not media:
            raise FileNotFoundError

        start = time.time()
        message = await f(document=media, **kwargs)
        logger.info(
            "%s\tSent message with media to user `%d` in %.2f s",
            f.__name__,
            kwargs["chat_id"],
            time.time() - start,
        )

        if not document and message:
            effective_file = (
                message.effective_attachment
                if not message or not isinstance(message.effective_attachment, tuple)
                else message.effective_attachment[-1]
            )
            set_file_id_cache(cache_key, effective_file.file_id)

    return inner


@get_or_set_file_id
async def send_message_with_animation(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    document: FileInput | None,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: ParseMode | None = None,
) -> Message | None:
    if document:
        try:
            return await context.bot.send_animation(
                chat_id=chat_id,
                animation=document,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except TelegramError as exc:
            logger.error(
                "Send message with animation for user `%d` error: %s", chat_id, exc
            )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


@get_or_set_file_id
async def send_message_with_photo(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    document: FileInput | None,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: ParseMode | None = None,
) -> Message | None:
    if document:
        try:
            return await context.bot.send_photo(
                chat_id=chat_id,
                photo=document,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except TelegramError as exc:
            logger.error("Send message media for user `%d` error: %s", chat_id, exc)
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


@get_or_set_file_id
async def edit_message_with_photo(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    text: str,
    document: FileInput | None,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: ParseMode | None = None,
) -> None:
    if document:
        try:
            return await context.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=document, caption=text, parse_mode=parse_mode
                ),
                reply_markup=reply_markup,
            )
        except TelegramError as exc:
            logger.error("Edit message media for user `%d` error: %s", chat_id, exc)

    else:
        try:
            return await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except TelegramError as exc:
            logger.error("Edit message for user `%d` error: %s", chat_id, exc)

    return await send_message_with_photo(
        context=context,
        chat_id=chat_id,
        text=text,
        document=document,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )
