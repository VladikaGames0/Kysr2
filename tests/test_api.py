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
        self.assertEqual(self.api.base_url, "https://api.hh.ru/vacancies")
        self.assertIn('User-Agent', self.api.headers)

    def test_get_vacancies_invalid_query(self):
        """Тест получения вакансий с неверным запросом"""
        # Пустой запрос должен вернуть пустой список или ошибку
        vacancies = self.api.get_vacancies("")
        self.assertIsInstance(vacancies, list)


if __name__ == '__main__':
    unittest.main()