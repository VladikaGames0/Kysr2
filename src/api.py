import requests
from src.abstract_classes import APIHandler
from typing import Dict, List, Any


class HeadHunterAPI(APIHandler):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"  # Приватный атрибут
        self.__headers = {'User-Agent': 'HH-User-Agent'}  # Приватный атрибут

    def get_vacancies(self, search_query: str, area: str = "113") -> List[Dict[str, Any]]:
        """
        Получить вакансии по поисковому запросу

        Args:
            search_query: Поисковый запрос
            area: Код региона (113 - Россия)

        Returns:
            Список вакансий в формате JSON
        """
        params = {
            'text': search_query,
            'area': area,
            'per_page': 100,
            'page': 0
        }

        try:
            # Используем приватный метод для подключения
            response = self.__connect_to_api(params)
            data = response.json()
            return data.get('items', [])
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

    def __connect_to_api(self, params: dict):
        """Приватный метод для подключения к API"""
        return requests.get(self.__base_url, params=params, headers=self.__headers)

    def get_vacancy_details(self, vacancy_id: str) -> Dict[str, Any]:
        """Получить детальную информацию о вакансии"""
        url = f"{self.__base_url}/{vacancy_id}"
        try:
            response = self.__connect_to_api({})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении деталей вакансии: {e}")
            return {}