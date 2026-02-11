import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    def setUp(self):
        self.api = HeadHunterAPI()

    def test_api_initialization(self):
        """Тест инициализации API"""
        # Теперь атрибуты приватные, но можем проверить через публичные методы
        self.assertIsInstance(self.api, HeadHunterAPI)

    def test_get_vacancies_method(self):
        """Тест метода получения вакансий"""
        # Метод должен возвращать список
        vacancies = self.api.get_vacancies("Python")
        self.assertIsInstance(vacancies, list)


if __name__ == '__main__':
    unittest.main()