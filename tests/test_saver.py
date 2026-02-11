import unittest
import sys
import os
import json
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.vacancy import Vacancy
from src.saver import JSONSaver


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        """Создание тестовых данных и временного файла"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_vacancies.json")

        self.saver = JSONSaver(self.test_file)

        self.vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python, Django",
            employer="Company A"
        )

        self.vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/124",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            description="Разработка на Java, Spring",
            employer="Company B"
        )

        self.vacancy3 = Vacancy(
            title="Frontend Developer",
            url="https://hh.ru/vacancy/125",
            salary={},  # Зарплата не указана
            description="Разработка на React, JavaScript",
            employer="Company C"
        )

    def tearDown(self):
        """Удаление временных файлов"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_vacancy(self):
        """Тест добавления вакансии"""
        self.saver.add_vacancy(self.vacancy1)

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.test_file))

        # Читаем файл и проверяем содержимое
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Python Developer")

    def test_add_duplicate_vacancy(self):
        """Тест добавления дублирующей вакансии"""
        self.saver.add_vacancy(self.vacancy1)
        self.saver.add_vacancy(self.vacancy1)  # Пытаемся добавить ту же вакансию

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Должна быть только одна вакансия
        self.assertEqual(len(data), 1)

    def test_add_multiple_vacancies(self):
        """Тест добавления нескольких вакансий"""
        vacancies = [self.vacancy1, self.vacancy2, self.vacancy3]
        self.saver.add_vacancies(vacancies)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 3)

    def test_get_vacancies(self):
        """Тест получения вакансий"""
        self.saver.add_vacancy(self.vacancy1)
        self.saver.add_vacancy(self.vacancy2)

        # Получаем все вакансии
        all_vacancies = self.saver.get_vacancies()
        self.assertEqual(len(all_vacancies), 2)

        # Фильтруем по ключевому слову
        filtered = self.saver.get_vacancies({"keyword": "Python"})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['title'], "Python Developer")

        # Фильтруем по названию
        filtered = self.saver.get_vacancies({"title": "Java"})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['title'], "Java Developer")

        # Фильтруем по минимальной зарплате
        filtered = self.saver.get_vacancies({"salary_min": 130000})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['title'], "Java Developer")

        # Тест с меньшей зарплатой - должны вернуться обе вакансии
        filtered = self.saver.get_vacancies({"salary_min": 100000})
        self.assertEqual(len(filtered), 2)

    def test_get_vacancies_no_criteria(self):
        """Тест получения вакансий без критериев"""
        self.saver.add_vacancy(self.vacancy1)
        vacancies = self.saver.get_vacancies()  # Без параметров
        self.assertEqual(len(vacancies), 1)

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        self.saver.add_vacancy(self.vacancy1)
        self.saver.add_vacancy(self.vacancy2)

        # Удаляем одну вакансию
        self.saver.delete_vacancy(self.vacancy1)

        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['title'], "Java Developer")

    def test_delete_nonexistent_vacancy(self):
        """Тест удаления несуществующей вакансии"""
        self.saver.add_vacancy(self.vacancy1)

        # Пытаемся удалить вакансию, которой нет в файле
        self.saver.delete_vacancy(self.vacancy2)

        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)

    def test_clear_file(self):
        """Тест очистки файла"""
        self.saver.add_vacancy(self.vacancy1)
        self.saver.add_vacancy(self.vacancy2)

        self.saver.clear_file()

        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)

    def test_get_top_vacancies_by_salary(self):
        """Тест получения топ вакансий по зарплате"""
        self.saver.add_vacancy(self.vacancy1)  # Средняя: 125000
        self.saver.add_vacancy(self.vacancy2)  # Средняя: 150000
        self.saver.add_vacancy(self.vacancy3)  # Средняя: 0

        top_vacancies = self.saver.get_top_vacancies_by_salary(1)
        self.assertEqual(len(top_vacancies), 1)
        self.assertEqual(top_vacancies[0]['title'], "Java Developer")

        top_vacancies = self.saver.get_top_vacancies_by_salary(2)
        self.assertEqual(len(top_vacancies), 2)
        # Проверяем сортировку по убыванию
        self.assertGreaterEqual(top_vacancies[0]['average_salary'], top_vacancies[1]['average_salary'])

        # Запрашиваем больше вакансий, чем есть
        top_vacancies = self.saver.get_top_vacancies_by_salary(10)
        self.assertEqual(len(top_vacancies), 2)  # Только вакансии с зарплатой > 0

    def test_empty_file(self):
        """Тест работы с пустым файлом"""
        # Создаем новый saver с несуществующим файлом
        new_saver = JSONSaver(os.path.join(self.test_dir, "empty.json"))

        # Должен вернуться пустой список
        vacancies = new_saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)

        # Удаление из пустого файла не должно вызывать ошибок
        new_saver.delete_vacancy(self.vacancy1)


if __name__ == '__main__':
    unittest.main()