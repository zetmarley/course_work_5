from src.search_employers import Search_employers
from src.employer_vacancies import Employer_vacancies
from src.dbmanager import DBManager

"""1. Найдем работодателей"""
employers = Search_employers.get_employers(input('Укажите ключевые слова для поиска работодателей: '),
                                           int(input('Укажите кол-во работодателей: ')))

"""2. Получим открытые вакансии работодателей"""
vacancies = Employer_vacancies.get_vacancies(employers)

"""3. Создадим БД и таблицы ей"""
DBManager.create_db()
DBManager.create_tables()

"""4. Заполним БД информацией о работодателях и об их вакансиях"""
DBManager.enter_data(vacancies)

"""Возвращает список из названий компаний и кол-во открытых вакансий"""
print('Работодатели и кол-во открытых вакансий: ')
for i in DBManager.get_companies_and_vacancies_count(): print(i)

"""Возвращает список всех вакансий"""
print('Открытые вакансии работодателей: ')
for i in DBManager.get_all_vacancies(): print(i)

"""Возвращает среднюю зарплату"""
print(DBManager.get_avg_salary())

"""Возвращает вакансии с повышенной зарплатой"""
print('Вакансии с повышенной зарплатой: ')
for i in DBManager.get_vacancies_with_higher_salary(): print(i)

"""Возвращает вакансии по ключевым словам"""
print(DBManager.get_vacancies_with_keyword(input('Поиск вакансий по ключевым словам\n'
                                                 'Введите ключевое слово: ')))