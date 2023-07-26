from datetime import datetime


class Vacancy:
    def __init__(self, vacancy: dict):
        """
        :param vacancy - словарь с информацией о вакансии
        """
        self.title = vacancy['title']
        self.employer = vacancy['employer']
        self.salary_from = vacancy['salary_from']
        self.salary_to = vacancy['salary_to']
        self.currency = vacancy['currency']
        self.currency_rate = vacancy['currency_rate']
        self.link = vacancy['link']
        self.town = vacancy['town']
        self.date = vacancy['date']

    def __repr__(self) -> str:
        """
        Возвращает представление вакансии в виде строки.

        :return: Представление вакансии в виде строки.
        """
        return f"Vacancy(title={self.title}, link={self.link}, employer ={self.employer}\n" \
               f"salary_from={self.salary_from}, salary_to={self.salary_to}, currency={self.currency}\n" \
               f"currency_rate = {self.currency_rate}, town={self.town}, date={self.date})"

    def __str__(self) -> str:
        """
        Возвращает строковое представление экземпляра класса Vacancy
        """
        # Различное представление строки 'зарплата' в зависимости от имеющихся данных
        if self.salary_from == 0 and self.salary_to != 0:
            self.salary_from = f' до {self.salary_to} {self.currency}'
        elif self.salary_to == 0 and self.salary_from != 0:
            self.salary_from = f'от {self.salary_from} {self.currency}'
        elif self.salary_to != 0 and self.salary_from != 0:
            self.salary_from = f'от {self.salary_from} до {self.salary_to} {self.currency}'
        elif self.salary_from == 0 and self.salary_to == 0:
            self.salary_from = 'Не указана'

        return f'{self.title}\nРаботодатель: {self.employer}\n' \
               f'зарплата: {self.salary_from}\n'\
               f'дата публикации: {self.date}\n' \
               f'ссылка на вакансию {self.link}\n'\
               f'{self.town}\n'

    @classmethod
    def initialize_from_api(cls, vacancies: list) -> list:
        """
        Инициализация экземпляров класса Vacancy из списка словарей.
        :param vacancies - список словарей с вакансиями.
        :return список экземпляров класса Vacancy
        """
        vacancies_object = []
        for vac in vacancies:
            vacancy = Vacancy(vac)
            vacancies_object.append(vacancy)
        return vacancies_object

    @classmethod
    def display_vacancies(cls, vacancies_object: list) -> None:
        """
        Функция для вывода на экран списка вакансий
        :param vacancies_object: список экземпляров класса Vacancy
        """
        for vacancy in vacancies_object:
            print(vacancy)

    def __lt__(self, other: 'Vacancy') -> bool:
        """
       Определяет порядок сортировки вакансий по зарплате.

       :param other: Другая вакансия для сравнения.
       :return: True, если текущая вакансия имеет меньшую зарплату, иначе False.
       """
        return self.salary_from < other.salary_from

    def __eq__(self, other: 'Vacancy') -> bool:
        """
        Проверяет, равны ли две вакансии по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если зарплаты равны, иначе False.
        """
        return self.salary_from == other.salary_from

    @staticmethod
    def sorted_vacancy_for_date(vacancies_object: list) -> None:
        """
        Функция сортирует список экземпляров по дате
        :param vacancies_object: список экземпляров класса Vacancy
        """
        vacancies_object.sort(key=lambda x: datetime.strptime(x.date, '%d.%m.%Y'), reverse=True)

    @staticmethod
    def sorted_vacancy_for_min_salary(vacancies_object: list) -> None:
        """
        Функция сортирует список экземпляров по минимальной зарплате
        :param vacancies_object: список экземпляров класса Vacancy
        """
        vacancies_object.sort(key=lambda x: x.salary_from * x.currency_rate, reverse=True)



