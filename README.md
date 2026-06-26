# Telegram-бот: сообщение по расписанию

Простой бот, который раз в час отправляет сообщение в Telegram.

## Что внутри

- `main.py` — код бота
- `requirements.txt` — зависимости
- `Procfile` — указывает Railway запускать бота как worker
- `.gitignore`

## Шаг 1. Создать бота в Telegram

1. Напишите [@BotFather](https://t.me/BotFather) в Telegram.
2. Отправьте команду `/newbot`, придумайте имя.
3. BotFather пришлёт **токен** вида `123456789:AAExxxxxxxxxxxxxxxxxx` — сохраните его.

## Шаг 2. Узнать свой CHAT_ID

1. Напишите своему боту любое сообщение (например, «привет»).
2. Откройте в браузере ссылку (вставьте свой токен):
   `https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates`
3. Найдите в ответе `"chat":{"id":...}` — это число и есть ваш `CHAT_ID`.

## Шаг 3. Залить на GitHub

Загрузите все эти файлы в новый репозиторий на GitHub.

## Шаг 4. Развернуть на Railway

1. Зайдите на [railway.app](https://railway.app), нажмите **New Project → Deploy from GitHub repo**.
2. Выберите свой репозиторий.
3. Откройте вкладку **Variables** и добавьте переменные окружения:

| Переменная         | Значение                                  |
|--------------------|-------------------------------------------|
| `BOT_TOKEN`        | токен от BotFather                        |
| `CHAT_ID`          | ваш chat id                               |
| `MESSAGE`          | (необязательно) текст сообщения           |
| `INTERVAL_SECONDS` | (необязательно) интервал в секундах, по умолчанию `3600` |

4. Railway сам соберёт проект и запустит бота.

Готово — бот будет отправлять сообщение каждый час.

## Проверить локально

```bash
pip install -r requirements.txt
export BOT_TOKEN=ваш_токен
export CHAT_ID=ваш_id
export INTERVAL_SECONDS=10   # для теста — раз в 10 секунд
python main.py
```
