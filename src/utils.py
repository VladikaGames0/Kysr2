from typing import List
from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтровать вакансии по ключевым словам

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = f"{vacancy.title} {vacancy.description} {vacancy.employer}".lower()
        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Получить вакансии по диапазону зарплат

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат в формате "min-max" или просто число

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    # Очищаем от пробелов
    salary_range = salary_range.strip()

    try:
        if "-" in salary_range:
            # Формат "min-max"
            min_salary_str, max_salary_str = salary_range.split("-")
            min_salary = int(min_salary_str.strip())
            max_salary = int(max_salary_str.strip())
        else:
            # Формат "число" - ищем вакансии с зарплатой от этого числа
            min_salary = int(salary_range)
            max_salary = float('inf')  # Без верхней границы

        filtered = []
        for vacancy in vacancies:
            avg_salary = vacancy.get_average_salary()
            if min_salary <= avg_salary <= max_salary:
                filtered.append(vacancy)

        return filtered

    except ValueError:
        print("Неверный формат зарплаты. Используйте формат: 100000 или 100000-200000")
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Отсортировать вакансии по зарплате (по убыванию)

    Args:
        vacancies: Список вакансий

    Returns:
        Отсортированный список вакансий
    """
    return sorted(vacancies, key=lambda x: x.get_average_salary(), reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получить топ N вакансий

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        Список топ N вакансий
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]):
    """
    Вывести вакансии в консоль

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\nВакансия #{i}:")
        print(vacancy)