import os
import re

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MESSAGE = os.environ.get(
    "MESSAGE",
    "Ваш паспорт RUMOS-GR0433959 передан в курьерскую компанию",
)

# Интервал между сообщениями в секундах (по умолчанию 60 = каждая минута)
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "60"))


async def send_periodic(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляется по таймеру каждые INTERVAL_SECONDS секунд."""
    await context.bot.send_message(chat_id=CHAT_ID, text=MESSAGE)


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Срабатывает сразу, когда вы пишете 'start' или '/start'."""
    await update.message.reply_text(MESSAGE)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # Реакция на команду /start
    app.add_handler(CommandHandler("start", on_start))
    # Реакция на обычный текст "start" (в любом регистре)
    app.add_handler(
        MessageHandler(filters.Regex(re.compile(r"^\s*start\s*$", re.IGNORECASE)), on_start)
    )

    # Таймер: первое сообщение сразу, далее каждые INTERVAL_SECONDS секунд
    app.job_queue.run_repeating(send_periodic, interval=INTERVAL_SECONDS, first=0)

    print("Бот запущен.", flush=True)
    app.run_polling()


if __name__ == "__main__":
    main()
