import asyncio
import logging
import os
from telegram import Bot
from telegram.error import TelegramError

# ==============================
# Переменные берутся из Railway Environment Variables
# ==============================
BOT_TOKEN = os.environ["BOT_TOKEN"]    # задаётся в Railway
CHAT_ID   = os.environ["CHAT_ID"]      # задаётся в Railway

MESSAGE   = "Ваш паспорт RUMOS-GR0433959 передан в курьерскую компанию"
INTERVAL  = 60  # секунды
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


async def send_loop():
    bot = Bot(token=BOT_TOKEN)
    me = await bot.get_me()
    log.info(f"Бот запущен: @{me.username}")
    log.info(f"Отправка в chat_id={CHAT_ID} каждые {INTERVAL} сек.")

    while True:
        try:
            await bot.send_message(chat_id=CHAT_ID, text=MESSAGE)
            log.info("Сообщение отправлено ✓")
        except TelegramError as e:
            log.error(f"Ошибка Telegram: {e}")
        except Exception as e:
            log.error(f"Неожиданная ошибка: {e}")

        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(send_loop())
