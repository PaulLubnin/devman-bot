import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv

API_DEVMAN_URL = 'https://dvmn.org/api'


def get_a_list_of_jobs(auth_token):
    """Функция делает запрос на получение списка работ."""
    url = f'{API_DEVMAN_URL}/user_reviews/'
    response = requests.get(url, headers=auth_token)
    response.raise_for_status()
    return response.json()


def long_polling(auth_token, timestamp=None):
    """Функция делает запросы для получения списка проверок."""
    url = f'{API_DEVMAN_URL}/long_polling/'
    payload = {'timestamp': timestamp}
    response = requests.get(url, headers=auth_token, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    """Запуск скрипта."""
    token = {'Authorization': f'Token {os.getenv("API_DEVMAN_TOKEN", None)}'}

    jobs = get_a_list_of_jobs(token)
    pprint(jobs)

    while True:
        try:
            jobs_check_list = long_polling(token)
            if jobs_check_list.get('status') == 'timeout':
                jobs_check_list = long_polling(token, jobs_check_list.get('timestamp_to_request'))
                pprint(jobs_check_list)
        except requests.ReadTimeout:
            print('Проверенных работ нету.')
        except requests.ConnectionError:
            print('Неполадки с интернетом. Восстановление соединения...')
            time.sleep(30)


if __name__ == '__main__':
    load_dotenv()
    main()
