import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

API_DEVMAN_URL = 'https://dvmn.org/api'


def get_server_response(auth_token=None, timestamp=None):
    """Функция делает запросы для получения списка проверок."""
    url = f'{API_DEVMAN_URL}/long_polling/'
    token = {'Authorization': f'Token {auth_token}'}
    payload = {'timestamp': timestamp}
    response = requests.get(url, headers=token, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    """Запуск скрипта."""
    load_dotenv()
    devman_token = os.getenv('API_DEVMAN_TOKEN')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(bot_token)

    request_timestamp = None
    while True:
        try:
            jobs_check_list = get_server_response(devman_token, request_timestamp)
            if jobs_check_list.get('status') == 'timeout':
                request_timestamp = jobs_check_list.get('timestamp_to_request')
            if jobs_check_list.get('status') == 'found':
                request_timestamp = jobs_check_list.get('last_attempt_timestamp')
                result = jobs_check_list.get('new_attempts')[0]
                bot.send_message(chat_id, f'У Вас проверили работу "{result["lesson_title"]}"\n'
                                          f'{result["lesson_url"]}')
                if not result['is_negative']:
                    bot.send_message(chat_id, 'Преподавателю всё понравилось, можно приступать к следующему уроку!')
                if result['is_negative']:
                    bot.send_message(chat_id, 'К сожалению в работе нашилсь ошибки.')
        except requests.ReadTimeout:
            continue
        except requests.ConnectionError:
            print('Неполадки с интернетом. Восстановление соединения...')
            time.sleep(30)
        except Exception as error:
            logging.exception(error)


if __name__ == '__main__':
    main()
