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

        self.vacancy2 = Vacancy(
            title="Senior Python Developer",
            url="https://hh.ru/vacancy/124",
            salary={"from": 200000, "to": 250000, "currency": "RUR"},
            description="Senior разработчик Python",
            employer="Company B"
        )

        self.vacancy3 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/125",
            salary={},  # Зарплата не указана
            description="Разработка на Java",
            employer="Company C"
        )

    def test_vacancy_creation(self):
        """Тест создания вакансии"""
        self.assertEqual(self.vacancy1.title, "Python Developer")
        self.assertEqual(self.vacancy1.url, "https://hh.ru/vacancy/123")
        self.assertEqual(self.vacancy1.employer, "Company A")

    def test_salary_validation(self):
        """Тест валидации зарплаты"""
        self.assertEqual(self.vacancy1.salary["from"], 100000)
        self.assertEqual(self.vacancy1.salary["to"], 150000)
        self.assertEqual(self.vacancy1.salary["currency"], "RUR")

        # Тест для вакансии без зарплаты
        self.assertEqual(self.vacancy3.salary["from"], 0)
        self.assertEqual(self.vacancy3.salary["to"], 0)
        self.assertEqual(self.vacancy3.salary["currency"], "Зарплата не указана")

    def test_average_salary(self):
        """Тест расчета средней зарплаты"""
        self.assertEqual(self.vacancy1.get_average_salary(), 125000.0)
        self.assertEqual(self.vacancy2.get_average_salary(), 225000.0)
        self.assertEqual(self.vacancy3.get_average_salary(), 0.0)

    def test_comparison_operators(self):
        """Тест операторов сравнения"""
        # vacancy2 должна быть больше vacancy1 по зарплате
        self.assertTrue(self.vacancy2 > self.vacancy1)
        self.assertTrue(self.vacancy1 < self.vacancy2)
        self.assertTrue(self.vacancy2 >= self.vacancy1)
        self.assertTrue(self.vacancy1 <= self.vacancy2)

        # vacancy3 должна быть меньше всех
        self.assertTrue(self.vacancy3 < self.vacancy1)
        self.assertTrue(self.vacancy3 < self.vacancy2)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy_dict = self.vacancy1.to_dict()
        self.assertEqual(vacancy_dict["title"], "Python Developer")
        self.assertEqual(vacancy_dict["average_salary"], 125000.0)
        self.assertIn("salary", vacancy_dict)
        self.assertIn("description", vacancy_dict)

    def test_str_representation(self):
        """Тест строкового представления"""
        str_repr = str(self.vacancy1)
        self.assertIn("Python Developer", str_repr)
        self.assertIn("Company A", str_repr)
        self.assertIn("100000-150000", str_repr)


if __name__ == '__main__':
    unittest.main()