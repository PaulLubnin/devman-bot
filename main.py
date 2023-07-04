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


def long_polling(auth_token):
    """Функция делает запросы с таймаутом."""
    url = f'{API_DEVMAN_URL}/long_polling/'
    response = requests.get(url, headers=auth_token, timeout=90)
    response.raise_for_status()
    return response.json()


def main():
    """Запуск скрипта."""
    token = {'Authorization': f'Token {os.getenv("API_DEVMAN_TOKEN", None)}'}

    jobs = get_a_list_of_jobs(token)
    pprint(jobs)

    while True:
        try:
            polling = long_polling(token)
            for elem in polling.items():
                pprint(elem)
        except requests.ReadTimeout:
            print('Проверенных работ нету.')
        except requests.ConnectionError:
            print('Неполадки с интернетом. Восстановление соединения...')
            time.sleep(30)


if __name__ == '__main__':
    load_dotenv()
    main()
