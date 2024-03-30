Всем привет, данная работа позволит вам создать БД и вносить в нее данные о работодателях и об их вакансиях из HH.ru

Инструкция:
Все необходимые функции можно применять в файле main.py

"""Поэтапная инструкция"""
"""1. Найдем работодателей"""
if __name__ == "__main__":
    employers = Search_employers.get_employers(input('Укажите ключевые слова для поиска работодателей: '),
                                               int(input('Укажите кол-во работодателей: ')))

"""2. Получим открытые вакансии работодателей"""
if __name__ == "__main__":
    vacancies = Employer_vacancies.get_vacancies(employers)

"""3. Создадим БД и таблицы ей"""
if __name__ == "__main__":
    DBManager.create_db()
    DBManager.create_tables()

"""4. Заполним БД информацией о работодателях и об их вакансиях"""
if __name__ == "__main__":
    DBManager.enter_data(vacancies)

"""Следующие методы позволят вам найти необходимуб инфу из БД"""

"""Возвращает список из названий компаний и кол-во открытых вакансий"""
if __name__ == "__main__":
    print(DBManager.get_companies_and_vacancies_count())

"""Возвращает список всех вакансий"""
if __name__ == "__main__":
    print(DBManager.get_all_vacancies())

"""Возвращает среднюю зарплату"""
if __name__ == "__main__":
    print(DBManager.get_avg_salary())

"""Возвращает вакансии с повышенной зарплатой"""
if __name__ == "__main__":
    print(DBManager.get_vacancies_with_higher_salary())

"""Возвращает вакансии по ключевым словам"""
if __name__ == "__main__":
    print(DBManager.get_vacancies_with_keyword(input('Введите ключевое слово для поиска: ')))
