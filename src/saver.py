import json
import os
from typing import List, Dict, Any
from src.abstract_classes import DataSaver
from src.vacancy import Vacancy


class JSONSaver(DataSaver):
    """Класс для сохранения вакансий в JSON файл"""

    def get_vacancies_by_salary_range(self, min_salary: float = 0, max_salary: float = float('inf')) -> List[
        Dict[str, Any]]:
        """
        Получить вакансии по диапазону зарплат

        Args:
            min_salary: Минимальная зарплата
            max_salary: Максимальная зарплата

        Returns:
            Отфильтрованный список вакансий
        """
        vacancies = self._load_vacancies()
        filtered = []

        for vacancy in vacancies:
            avg_salary = vacancy.get('average_salary', 0)
            if min_salary <= avg_salary <= max_salary:
                filtered.append(vacancy)

        return filtered
    def __init__(self, filename: str = "data/vacancies.json"):
        self.filename = filename
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Создать директорию, если она не существует"""
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def add_vacancy(self, vacancy: Vacancy):
        """Добавить вакансию в файл"""
        vacancies = self._load_vacancies()

        # Проверяем, есть ли уже такая вакансия
        vacancy_dict = vacancy.to_dict()
        if vacancy_dict not in vacancies:
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)
            print(f"Вакансия '{vacancy.title}' добавлена.")
        else:
            print(f"Вакансия '{vacancy.title}' уже существует в файле.")

    def add_vacancies(self, vacancies: List[Vacancy]):
        """Добавить несколько вакансий в файл"""
        existing_vacancies = self._load_vacancies()
        new_vacancies = []

        for vacancy in vacancies:
            vacancy_dict = vacancy.to_dict()
            if vacancy_dict not in existing_vacancies:
                new_vacancies.append(vacancy_dict)

        if new_vacancies:
            existing_vacancies.extend(new_vacancies)
            self._save_vacancies(existing_vacancies)
            print(f"Добавлено {len(new_vacancies)} вакансий.")
        else:
            print("Нет новых вакансий для добавления.")

    def get_vacancies(self, criteria: dict = None) -> List[Dict[str, Any]]:
        """
        Получить вакансии по критериям

        Args:
            criteria: Словарь с критериями поиска

        Returns:
            Список вакансий, удовлетворяющих критериям
        """
        vacancies = self._load_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True

            for key, value in criteria.items():
                if key == "salary_min":
                    avg_salary = vacancy.get("average_salary", 0)
                    if avg_salary < float(value):
                        match = False
                        break

                elif key == "keyword" and value:
                    vacancy_text = f"{vacancy.get('title', '')} {vacancy.get('description', '')} {vacancy.get('employer', '')}".lower()
                    if value.lower() not in vacancy_text:
                        match = False
                        break

                elif key == "title" and value:
                    title = vacancy.get('title', '').lower()
                    if value.lower() not in title:
                        match = False
                        break

                elif key in vacancy and vacancy[key] != value:
                    match = False
                    break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy):
        """Удалить вакансию из файла"""
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        if vacancy_dict in vacancies:
            vacancies.remove(vacancy_dict)
            self._save_vacancies(vacancies)
            print(f"Вакансия '{vacancy.title}' удалена.")
        else:
            print(f"Вакансия '{vacancy.title}' не найдена в файле.")

    def clear_file(self):
        """Очистить файл с вакансиями"""
        self._save_vacancies([])
        print("Файл с вакансиями очищен.")

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузить вакансии из файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]):
        """Сохранить вакансии в файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)

    def get_top_vacancies_by_salary(self, n: int) -> List[Dict[str, Any]]:
        """
        Получить топ N вакансий по зарплате

        Args:
            n: Количество вакансий для возврата

        Returns:
            Список топ N вакансий
        """
        vacancies = self._load_vacancies()
        # Фильтруем вакансии с ненулевой зарплатой
        vacancies_with_salary = [v for v in vacancies if v.get('average_salary', 0) > 0]
        sorted_vacancies = sorted(vacancies_with_salary, key=lambda x: x.get('average_salary', 0), reverse=True)
        return sorted_vacancies[:n]


class CSVSaver(DataSaver):
    """Класс для сохранения вакансий в CSV файл (заглушка)"""

    def add_vacancy(self, vacancy):
        print("CSV сохранение не реализовано")

    def get_vacancies(self, criteria: dict = None):
        print("CSV чтение не реализовано")
        return []

    def delete_vacancy(self, vacancy):
        print("CSV удаление не реализовано")

    def clear_file(self):
        print("CSV очистка не реализовано")


class TXTSaver(DataSaver):
    """Класс для сохранения вакансий в TXT файл (заглушка)"""

    def add_vacancy(self, vacancy):
        print("TXT сохранение не реализовано")

    def get_vacancies(self, criteria: dict = None):
        print("TXT чтение не реализовано")
        return []

    def delete_vacancy(self, vacancy):
        print("TXT удаление не реализовано")

    def clear_file(self):
        print("TXT очистка не реализовано")