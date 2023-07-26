from src.vacancyAPI import HeadHunterAPI, SuperJobAPI
from src.savervacancy import JSONSaver, TXTSaver
from src.vacancy import Vacancy


def user_interaction():
    # Создаем пустой список вакансий
    vacancies = []

    print("Приветствуем Вас на сервисе подбора вакансий")
    vacancy_title_user = input("Введите название интересующей профессии")

    # Создаем экземпляры классов для работы с API
    hh_api = HeadHunterAPI(vacancy_title_user)
    sj_api = SuperJobAPI(vacancy_title_user)

    # Наполняем список вакансий вакансиями, полученными от API
    for api in (hh_api, sj_api):
        api.get_vacancies(pages_count=1)
        vacancies.extend(api.get_form_vacancies())

    # Создаем экземпляры класса JSONSaver и TXTSaver для сохранения найденных вакансий в файл
    js_saver = JSONSaver('vacancies.json')
    txt_saver = TXTSaver('vacancies.txt')

    # Основной цикл программы
    while True:
        # Создаем список экземпляров класса Vacancy
        list_of_vacancies = Vacancy.initialize_from_api(vacancies)

        user_command = input(
            "Доступные команды.\n"
            "1 - вывести список вакансий\n"
            "2 - отсортировать по дате\n"
            "3 - отсортировать по минимальной зарплате\n"
            "4 - сохранить вакансии в файл\n"
            "5 - вывести вакансии от min зарплаты\n"
            "0 - выход\n"
        )
        if user_command == "1":
            print(f"Найдено {len(list_of_vacancies)} вакансий")
            Vacancy.display_vacancies(list_of_vacancies)

        if user_command == "2":
            Vacancy.sorted_vacancy_for_date(list_of_vacancies)
            Vacancy.display_vacancies(list_of_vacancies)

        if user_command == "3":
            Vacancy.sorted_vacancy_for_min_salary(list_of_vacancies)
            Vacancy.display_vacancies(list_of_vacancies)

        if user_command == "4":
            js_saver.save(vacancies)
            txt_saver.save(list_of_vacancies)
            print("Вакансии успешно записаны в файлы\n")

        if user_command == "5":
            min_salary = int(input("Введите минимально допустимую зарплату\n"))
            list_of_vacancies = [vacancy for vacancy in list_of_vacancies if vacancy.salary_from * vacancy.currency_rate > min_salary]
            print(f"Найдено {len(list_of_vacancies)} вакансий\n")
            Vacancy.display_vacancies(list_of_vacancies)

        if user_command not in "012345":
            print("Команда не может быть распознана.\n")
            continue

        if user_command == "0":
            break


if __name__ == "__main__":
    user_interaction()
