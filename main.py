import os
import re

from telegram import Update
from telegram.error import Forbidden, BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

MESSAGE = os.environ.get("MESSAGE", "Привет, я бот")

# Интервал между сообщениями в секундах (по умолчанию 60 = каждая минута)
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "60"))

# Множество всех, кто нажал "start". Хранится в памяти,
# при перезапуске контейнера на Railway список обнуляется.
subscribers: set[int] = set()


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Регистрирует пользователя, который написал 'start' или '/start'."""
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await update.message.reply_text(MESSAGE)


async def on_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Позволяет человеку отписаться командой /stop."""
    chat_id = update.effective_chat.id
    subscribers.discard(chat_id)
    await update.message.reply_text("Окей, больше не пишу 🙂")


async def broadcast(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Раз в INTERVAL_SECONDS отправляет сообщение всем подписчикам."""
    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id=chat_id, text=MESSAGE)
        except (Forbidden, BadRequest):
            # Человек заблокировал бота или удалил чат — убираем из списка
            subscribers.discard(chat_id)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(CommandHandler("stop", on_stop))
    app.add_handler(
        MessageHandler(filters.Regex(re.compile(r"^\s*start\s*$", re.IGNORECASE)), on_start)
    )

    app.job_queue.run_repeating(broadcast, interval=INTERVAL_SECONDS, first=INTERVAL_SECONDS)

    print("Бот запущен.", flush=True)
    app.run_polling()


if __name__ == "__main__":
    main()
