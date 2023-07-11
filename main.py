import os
import time

import requests
import telegram
from dotenv import load_dotenv

API_DEVMAN_URL = 'https://dvmn.org/api'


def long_polling(auth_token, timestamp=None):
    """Функция делает запросы для получения списка проверок."""
    url = f'{API_DEVMAN_URL}/long_polling/'
    payload = {'timestamp': timestamp}
    response = requests.get(url, headers=auth_token, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    """Запуск скрипта."""
    devman_token = {'Authorization': f'Token {os.getenv("API_DEVMAN_TOKEN", None)}'}
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(bot_token)

    while True:
        try:
            jobs_check_list = long_polling(devman_token)
            if jobs_check_list.get('status') == 'timeout':
                long_polling(devman_token, jobs_check_list.get('timestamp_to_request'))
            if jobs_check_list.get('status') == 'found':
                bot.send_message(chat_id, f'У Вас проверили работу "{jobs_check_list.get("new_attempts")[0]["lesson_title"]}"\n'
                                          f'{jobs_check_list.get("new_attempts")[0]["lesson_url"]}')
                if not jobs_check_list.get('new_attempts')[0]['is_negative']:
                    bot.send_message(chat_id, 'Преподавателю всё понравилось, можно приступать к следующему уроку!')
                if jobs_check_list.get('new_attempts')[0]['is_negative']:
                    bot.send_message(chat_id, 'К сожалению в работе нашилсь ошибки.')
        except requests.ReadTimeout:
            print('Проверенных работ нету.')
        except requests.ConnectionError:
            print('Неполадки с интернетом. Восстановление соединения...')
            time.sleep(30)


if __name__ == '__main__':
    load_dotenv()
    main()
