# Бот для подключения к API devman'а.

Склонируйте проект.

Создайте файл `.env`, в нем определите переменные:
- `API_DEVMAN_TOKEN` и присвойте ей токен, полученный [тут](https://dvmn.org/api/docs/);
- `TELEGRAM_BOT_TOKEN` токен телеграм бота;
- `TELEGRAM_CHAT_ID` номер чата;

Скрипт запускается командой:
```
python main.py
```