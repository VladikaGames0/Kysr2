from abc import ABC, abstractmethod


class APIHandler(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, search_query: str):
        """Получить вакансии по поисковому запросу"""
        pass


class DataSaver(ABC):
    """Абстрактный класс для сохранения вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавить вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict = None):
        """Получить вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """Удалить вакансию из файла"""
        pass

    @abstractmethod
    def clear_file(self):
        """Очистить файл с вакансиями"""
        pass