# Бот для подключения к API devman'а.

## Как установить
Для установки необходим [Python>=3.10](https://www.python.org/downloads/) и [git](https://git-scm.com/downloads).
После установки Python и Git можно приступать к установке библиотеки на компьютер.

Склонируйте проект:
```
https://github.com/PaulLubnin/devman-bot.git
```
В папке с проектом создайте отдельную среду для установки всех зависимостей, затем активируйте её:

- если у вас установлен только один Python:
```
python -m venv env
```
- если у вас установлены несколько разных версии Python:
```
py -3.10 -m venv env
```
- активируйте виртуальную среду:
```
env\Scripts\activate
```
Затем из папки с проектом в командной строке наберите и установите необходимые зависимости:
```
pip install -r requirements.txt
```

Создайте `.env` файл, в нем определите переменные:
- `API_DEVMAN_TOKEN` и присвойте ей токен, полученный [тут](https://dvmn.org/api/docs/);
- `TELEGRAM_BOT_TOKEN` токен телеграм бота, полученный от [Отца Ботов](https://telegram.me/BotFather);
- `TELEGRAM_CHAT_ID` номер чата, полученный у специального [бота](https://telegram.me/userinfobot);

## Как запустить:
```
python main.py
```
При правильной установке, бот будет в режиме ожидания пинговать ответы сервера.
Когда работа будет проверена, в чат с ботом придет сообщение о результате.