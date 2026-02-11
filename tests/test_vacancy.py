import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def setUp(self):
        """Создание тестовых вакансий"""
        self.vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python, Django",
            employer="Company A"
        )

    def test_vacancy_has_slots(self):
        """Тест наличия __slots__"""
        self.assertTrue(hasattr(self.vacancy1, '__slots__'))

        # Проверяем, что нельзя добавить новый атрибут
        with self.assertRaises(AttributeError):
            self.vacancy1.new_attribute = "test"

    def test_slots_content(self):
        """Тест содержимого __slots__"""
        expected_slots = ('title', 'url', 'salary', 'description', 'employer')
        self.assertEqual(self.vacancy1.__slots__, expected_slots)

    def test_memory_efficiency(self):
        """Тест экономии памяти (проверяем наличие __dict__)"""
        # У объектов с __slots__ не должно быть __dict__
        self.assertFalse(hasattr(self.vacancy1, '__dict__'))

    # ... остальные тесты остаются без изменений


if __name__ == '__main__':
    unittest.main()