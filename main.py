import os
import time
from datetime import datetime

import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MESSAGE = os.environ.get(
    "MESSAGE",
    "Ваш паспорт RUMOS-GR0433959 передан в курьерскую компанию",
)

# Интервал между сообщениями в секундах (по умолчанию 1 час = 3600 секунд)
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "3600"))


def send_message(text: str) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    print("Бот запущен. Отправка каждые", INTERVAL_SECONDS, "секунд.", flush=True)
    while True:
        try:
            send_message(MESSAGE)
            print(f"[{datetime.now().isoformat()}] Сообщение отправлено", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[{datetime.now().isoformat()}] Ошибка: {error}", flush=True)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
