import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()
API_DEVMAN_URL = 'https://dvmn.org/api'
AUTH_TOKEN = os.getenv('API_DEVMAN_TOKEN', None)


def get_a_list_of_jobs():
    """Функция делает запрос на получение списка работ."""
    url = f'{API_DEVMAN_URL}/user_reviews/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    """Запуск скрипта."""
    jobs = get_a_list_of_jobs()

    pprint(jobs)


if __name__ == '__main__':
    main()
