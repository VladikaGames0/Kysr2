from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.saver import JSONSaver
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies, print_vacancies, get_vacancies_by_salary
import os


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    # Шаг 1: Получение поискового запроса
    search_query = input("\nВведите поисковый запрос (например: Python разработчик): ").strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    # Шаг 2: Получение вакансий с HH.ru
    print("\nПолучение вакансий с HH.ru...")
    hh_api = HeadHunterAPI()
    vacancies_json = hh_api.get_vacancies(search_query)

    if not vacancies_json:
        print("По вашему запросу вакансии не найдены.")
        return

    # Шаг 3: Преобразование в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(vacancies_json)
    print(f"Найдено {len(vacancies_list)} вакансий.")

    if not vacancies_list:
        print("Не удалось обработать найденные вакансии.")
        return

    # Шаг 4: Сохранение в файл
    saver = JSONSaver()
    saver.add_vacancies(vacancies_list)

    # Шаг 5: Фильтрация по ключевым словам
    filter_input = input("\nВведите ключевые слова для фильтрации (через запятую): ").strip()
    filter_words = [word.strip() for word in filter_input.split(",")] if filter_input else []

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    print(f"После фильтрации осталось {len(filtered_vacancies)} вакансий.")

    # Шаг 6: Фильтрация по зарплате
    while True:
        salary_filter = input(
            "\nВведите минимальную зарплату или диапазон (например: 100000 или 100000-200000): ").strip()

        if not salary_filter:
            print("Пропускаем фильтрацию по зарплате.")
            ranged_vacancies = filtered_vacancies
            break
        else:
            ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_filter)
            if ranged_vacancies:
                print(f"После фильтрации по зарплате осталось {len(ranged_vacancies)} вакансий.")
                break
            else:
                print("Нет вакансий с указанной зарплатой. Попробуйте другой диапазон.")
                continue

    # Шаг 7: Сортировка и выбор топ N
    sorted_vacancies = sort_vacancies(ranged_vacancies)

    try:
        top_n_input = input("\nСколько топ вакансий показать? (по умолчанию 10): ").strip()
        top_n = int(top_n_input) if top_n_input else 10
    except ValueError:
        print("Некорректное число. Используется значение по умолчанию (10).")
        top_n = 10

    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Шаг 8: Вывод результатов
    print(f"\n{'=' * 60}")
    print(f"ТОП-{len(top_vacancies)} ВАКАНСИЙ ПО ЗАРПЛАТЕ:")
    print(f"{'=' * 60}")

    if top_vacancies:
        print_vacancies(top_vacancies)

        # Дополнительные опции
        while True:
            print("\n" + "=" * 60)
            print("ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ:")
            print("1. Показать все сохраненные вакансии")
            print("2. Найти вакансии по ключевому слову в описании")
            print("3. Получить топ N вакансий из сохраненных")
            print("4. Очистить файл с вакансиями")
            print("5. Выполнить новый поиск")
            print("6. Выход")

            choice = input("\nВыберите действие (1-6): ").strip()

            if choice == "1":
                all_vacancies = saver.get_vacancies()
                print(f"\nВсего сохранено {len(all_vacancies)} вакансий:")

                # Предлагаем отсортировать
                sort_by = input("Отсортировать по зарплате? (да/нет): ").strip().lower()
                if sort_by == 'да':
                    all_vacancies_sorted = sorted(all_vacancies, key=lambda x: x.get('average_salary', 0), reverse=True)
                    all_vacancies = all_vacancies_sorted

                for i, vac in enumerate(all_vacancies[:20], 1):
                    salary_from = vac['salary']['from'] if vac['salary']['from'] else 0
                    salary_to = vac['salary']['to'] if vac['salary']['to'] else 0
                    salary_currency = vac['salary']['currency']

                    if salary_currency == "Зарплата не указана":
                        salary_str = "Зарплата не указана"
                    else:
                        salary_str = f"{salary_from}-{salary_to} {salary_currency}"

                    avg_salary = vac.get('average_salary', 0)
                    print(f"{i}. {vac['title']} - {salary_str} (средняя: {avg_salary:.0f})")

            elif choice == "2":
                keyword = input("Введите ключевое слово для поиска в описании: ").strip()
                if keyword:
                    found = saver.get_vacancies({"keyword": keyword})
                    print(f"\nНайдено {len(found)} вакансий с ключевым словом '{keyword}':")
                    for i, vac in enumerate(found[:10], 1):
                        print(f"{i}. {vac['title']}")
                else:
                    print("Ключевое слово не введено.")

            elif choice == "3":
                try:
                    n = int(input("Введите количество вакансий для топа: ").strip())
                    top_vacancies_json = saver.get_top_vacancies_by_salary(n)
                    print(f"\nТоп-{len(top_vacancies_json)} вакансий по зарплате:")
                    for i, vac in enumerate(top_vacancies_json, 1):
                        salary_from = vac['salary']['from'] if vac['salary']['from'] else 0
                        salary_to = vac['salary']['to'] if vac['salary']['to'] else 0
                        salary_currency = vac['salary']['currency']

                        if salary_currency == "Зарплата не указана":
                            salary_str = "Зарплата не указана"
                        else:
                            salary_str = f"{salary_from}-{salary_to} {salary_currency}"

                        avg_salary = vac.get('average_salary', 0)
                        print(f"{i}. {vac['title']} - {salary_str} (средняя: {avg_salary:.0f})")
                except ValueError:
                    print("Некорректное число.")

            elif choice == "4":
                confirm = input("Вы уверены, что хотите очистить файл? (да/нет): ").strip().lower()
                if confirm == 'да':
                    saver.clear_file()
                    print("Файл очищен.")

            elif choice == "5":
                print("\n" + "=" * 60)
                print("НОВЫЙ ПОИСК")
                print("=" * 60)
                user_interaction()
                break

            elif choice == "6":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    else:
        print("Нет вакансий, соответствующих критериям.")


if __name__ == "__main__":
    user_interaction()