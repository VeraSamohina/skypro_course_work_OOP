from abc import ABC, abstractmethod
import os
import requests
from datetime import datetime
from utils.currency import currency_exchange

SJ_API_KEY = os.getenv('SUPER_JOB_API_KEY')


class VacancyAPI(ABC):
    """
    Класс для представления API для работы с вакансиями
    """
    params = None

    @abstractmethod
    def get_request(self):
        pass

    def get_vacancies(self, pages_count=2) -> None:
        """
        Добавление вакансий, полученных с каждой страницы в общий список вакансий
        :param pages_count: количество страниц для получения вакансий
        """
        self.vacancies = []
        for page in range(pages_count):
            self.params['page'] = page
            page_vacancies = self.get_request()
            self.vacancies.extend(page_vacancies)
            print(f'Добавлено {len(page_vacancies)} вакансий')
            if len(page_vacancies) == 0:
                break

    @abstractmethod
    def get_form_vacancies(self):
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для получения информации от API HeadHunter
    """
    url = 'https://api.hh.ru/vacancies/'

    def __init__(self, vacancy_title: str) -> None:
        """
        :param vacancy_title: Название вакансии, по которому будет производиться поиск
        """
        self.params = {
            'text': vacancy_title,
            'page': None,
            'per_page': 100,
            'archived': False
        }

    def get_request(self) -> list:
        """
        Функция для запроса вакансий с API hh.ru по выбранной вакансии
        :return: список словарей с найденными вакансиями
        """
        response = requests.get(self.url, params=self.params)
        data_vacancy = response.json()
        return data_vacancy['items']

    def get_form_vacancies(self) -> list:
        """
        Функция для формирования из списка, полученного от API, списка словарей с унифицированными ключами,
         необходимыми для дальнейшей работы
        :return: список словарей с вакансиями
        """
        form_vacancies = []

        for vacancy in self.vacancies:
            if vacancy['salary'] is not None:
                # Для валюты, отличной от рубля, получаем курс для возможности сравнения зарплат между собой
                if vacancy['salary']['currency'] != 'RUR':
                    currency_rate = currency_exchange(vacancy['salary']['currency'])
                else:
                    currency_rate = 1

                form_vacancy = {
                    'title': vacancy['name'],
                    'employer': vacancy['employer']['name'],
                    'salary_from': vacancy['salary']['from'] if vacancy['salary']['from'] else 0,
                    'salary_to': vacancy['salary']['to'] if vacancy['salary']['to'] else 0,
                    'currency': vacancy['salary']['currency'] if vacancy['salary']['currency'] != 'RUR' else 'рублей',
                    'currency_rate': currency_rate,
                    'link': vacancy['alternate_url'],
                    'town': vacancy['area']['name'],
                    'date': datetime.fromisoformat(vacancy["published_at"]).strftime('%d.%m.%Y')
                    }
            else:
                # Для словарей, в которых не указана зарплата, устанавливаем ее равной 0 для возможности сравнения
                form_vacancy = {
                    'title': vacancy['name'],
                    'employer': vacancy['employer']['name'],
                    'salary_from': 0,
                    'salary_to': 0,
                    'currency': None,
                    'currency_rate': 0,
                    'link': vacancy['alternate_url'],
                    'town': vacancy['area']['name'],
                    'date': datetime.fromisoformat(vacancy["published_at"]).strftime('%d.%m.%Y')
                }
            form_vacancies.append(form_vacancy)
        return form_vacancies


class SuperJobAPI(VacancyAPI):
    """
    Класс для работы с API SuperJob
    """
    url = 'https://api.superjob.ru/2.0/vacancies'

    def __init__(self, vacancy_title: str) -> None:
        """
        :param vacancy_title: Ключевое слово - название вакансии, по которому будет производиться поиск
        """
        self.headers = {'X-Api-App-Id': SJ_API_KEY}
        self.params = {
            'keyword': vacancy_title,
            'count': 100,
            'page': None,
            'archive': False
        }
        self.vacancies = []

    def get_request(self) -> list:
        """
       Функция для получения вакансий с API superjob.ru по выбранному ключевому слову(название вакансии)
       :return: список словарей с найденными вакансиями
       """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data_vacancy = response.json()
        return data_vacancy['objects']

    def get_form_vacancies(self):
        """
        Функция для формирования из списка, полученного от API, списка словарей с унифицированными ключами,
         необходимыми для дальнейшей работы
        :return: список словарей с вакансиями
        """
        form_vacancies = []

        for vacancy in self.vacancies:
            # Для валюты, отличной от рубля, получаем курс для возможности сравнения зарплат между собой
            if vacancy['currency'] != 'rub':
                currency_rate = currency_exchange(vacancy['salary']['currency'].upper)
            else:
                currency_rate = 1
            form_vacancy = {
                'title': vacancy['profession'],
                'employer': vacancy['firm_name'],
                'salary_from': vacancy['payment_from'] if vacancy['payment_from'] else 0,
                'salary_to': vacancy['payment_to'] if vacancy['payment_to'] else 0,
                'currency': vacancy['currency'] if vacancy['currency'] != 'rub' else 'рублей',
                'currency_rate': currency_rate,
                'link': vacancy['link'],
                'town': vacancy['town']['title'],
                'date': datetime.utcfromtimestamp(vacancy['date_published']).strftime('%d.%m.%Y')
                }
            form_vacancies.append(form_vacancy)
        return form_vacancies
