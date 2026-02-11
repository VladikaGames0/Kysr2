class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ('title', 'url', 'salary', 'description', 'employer')  # Экономия памяти

    def __init__(self, title: str, url: str, salary: dict, description: str, employer: str = ""):
        """
        Инициализация вакансии

        Args:
            title: Название вакансии
            url: Ссылка на вакансию
            salary: Зарплата в формате словаря
            description: Описание вакансии
            employer: Работодатель
        """
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description
        self.employer = employer
        self._validate_data()

    def _validate_salary(self, salary_data: dict) -> dict:
        """Валидация данных о зарплате"""
        if not salary_data:
            return {"from": 0, "to": 0, "currency": "Зарплата не указана"}

        validated_salary = {
            "from": salary_data.get("from") or 0,
            "to": salary_data.get("to") or 0,
            "currency": salary_data.get("currency", "Не указана")
        }

        # Если зарплата не указана
        if validated_salary["from"] == 0 and validated_salary["to"] == 0:
            validated_salary["currency"] = "Зарплата не указана"

        return validated_salary

    def _validate_data(self):
        """Валидация всех данных вакансии"""
        if not self.title:
            raise ValueError("Название вакансии не может быть пустым")
        if not self.url:
            raise ValueError("URL вакансии не может быть пустым")

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_from = self.salary['from'] if self.salary['from'] else 0
        salary_to = self.salary['to'] if self.salary['to'] else 0

        if self.salary['currency'] == "Зарплата не указана":
            salary_str = "Зарплата не указана"
        else:
            salary_str = f"{salary_from}-{salary_to} {self.salary['currency']}"

        return (f"{self.title}\n"
                f"Работодатель: {self.employer}\n"
                f"Зарплата: {salary_str}\n"
                f"Ссылка: {self.url}\n"
                f"Описание: {self.description[:100]}...\n"
                f"{'-' * 50}")

    def __repr__(self) -> str:
        return f"Vacancy('{self.title}', '{self.url}', {self.salary})"

    def __eq__(self, other) -> bool:
        """Проверка на равенство по средней зарплате"""
        if not isinstance(other, Vacancy):
            return False
        return self.get_average_salary() == other.get_average_salary()

    def __lt__(self, other) -> bool:
        """Проверка на меньше по средней зарплате"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.get_average_salary() < other.get_average_salary()

    def __le__(self, other) -> bool:
        """Проверка на меньше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.get_average_salary() <= other.get_average_salary()

    def __gt__(self, other) -> bool:
        """Проверка на больше по средней зарплате"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.get_average_salary() > other.get_average_salary()

    def __ge__(self, other) -> bool:
        """Проверка на больше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self.get_average_salary() >= other.get_average_salary()

    def get_average_salary(self) -> float:
        """Получить среднюю зарплату"""
        if self.salary["from"] == 0 and self.salary["to"] == 0:
            return 0.0

        if self.salary["from"] and self.salary["to"]:
            return (float(self.salary["from"]) + float(self.salary["to"])) / 2
        elif self.salary["from"]:
            return float(self.salary["from"])
        elif self.salary["to"]:
            return float(self.salary["to"])
        else:
            return 0.0

    @classmethod
    def cast_to_object_list(cls, vacancies_json: list) -> list:
        """
        Преобразовать JSON вакансий в список объектов Vacancy

        Args:
            vacancies_json: Список вакансий в формате JSON

        Returns:
            Список объектов Vacancy
        """
        vacancies_list = []

        for vacancy_data in vacancies_json:
            try:
                # Извлекаем данные из JSON
                title = vacancy_data.get('name', '')
                url = vacancy_data.get('alternate_url', '')

                # Обрабатываем зарплату
                salary_data = vacancy_data.get('salary')
                if salary_data:
                    salary = {
                        "from": salary_data.get('from'),
                        "to": salary_data.get('to'),
                        "currency": salary_data.get('currency', '')
                    }
                else:
                    salary = {}

                # Обрабатываем описание
                snippet = vacancy_data.get('snippet', {})
                description = f"{snippet.get('requirement', '')} {snippet.get('responsibility', '')}"

                # Обрабатываем работодателя
                employer_data = vacancy_data.get('employer', {})
                employer = employer_data.get('name', '')

                # Создаем объект Vacancy
                vacancy = cls(title, url, salary, description.strip(), employer)
                vacancies_list.append(vacancy)

            except Exception as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies_list

    def to_dict(self) -> dict:
        """Преобразовать вакансию в словарь"""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "employer": self.employer,
            "average_salary": float(self.get_average_salary())
        }