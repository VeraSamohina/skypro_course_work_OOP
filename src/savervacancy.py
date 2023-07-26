import json
from abc import ABC, abstractmethod


class SaverVacancy(ABC):
    """Абстрактный класс для сохранения найденных вакансий"""

    def __init__(self, file_path):
        """
        :param file_path: путь к файлу
        """
        self.file_path = file_path

    @abstractmethod
    def save(self, *args, **kwargs):
        pass


class JSONSaver(SaverVacancy):
    """
    Класс для сохранения вакансий в json - файл
    """
    def save(self, vacancy_data):
        with open(self.file_path, 'w', encoding="utf-8") as f:
            for vacancy in vacancy_data:
                json.dump(str(vacancy), f, indent=2, ensure_ascii=False)
                f.write('\n')

class TXTSaver(SaverVacancy):
    """
    Класс для сохранения вакансий в текстовом формате
    """
    def save(self, vacancy_data):
        with open(self.file_path, 'w', encoding="utf-8") as f:
            for vacancy in vacancy_data:
                f.write(str(vacancy))
                f.write('\n')
