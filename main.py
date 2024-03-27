import requests
import json
import psycopg2

class HH_API():

    url = 'https://api.hh.ru/employers'
    response = requests.get(url)
    page = json.loads(response.text)

    def __init__(self):
        pass

    @classmethod
    def get_employers(cls):
        box = []
        for i in cls.page['items']:
            box.append(i)
        return box

class Search_employers():

    def __init__(self):
        pass

    @classmethod
    def get_employers(cls, search_query, quantity=10):
        employers_list = []
        employers = json.loads(requests.get(HH_API.url, params={'text': search_query,
                                                           'per_page': quantity,
                                                           'only_with_vacancies': True}).text)['items']
        for i in employers:
            employers_data = {}
            employers_data['company_name'] = i['name']
            employers_data['open_vacancies'] = i['open_vacancies']
            employers_data['vacancies_url'] = i['vacancies_url']
            employers_list.append(employers_data)
        return employers_list

class Employer_vacancies():

    def __init__(self):
        pass

    @classmethod
    def get_vacancies(cls, employers_list):
        box = []
        for i in employers_list:
            count = 1
            url = i['vacancies_url']
            response = requests.get(url)
            page = json.loads(response.text)
            vacancies = {}
            vacancies['employer'] = i
            vacancy_box = []
            for i in page['items']:
                vacancy_to = {}
                vacancy_to['vacancy_num'] = count
                vacancy_to['vacancy_name'] = i['name']
                try:
                    vacancy_to['salary_from'] = i['salary']['from']
                except TypeError:
                    vacancy_to['salary_from'] = None
                try:
                    vacancy_to['salary_to'] = i['salary']['to']
                except TypeError:
                    vacancy_to['salary_to'] = None
                try:
                    vacancy_to['salary_currency'] = i['salary']['currency']
                except TypeError:
                    vacancy_to['salary_currency'] = None
                try:
                    vacancy_to['city'] = i['address']['city']
                except TypeError:
                    vacancy_to['city'] = None
                try:
                    vacancy_to['street'] = i['address']['street']
                except TypeError:
                    vacancy_to['street'] = None
                try:
                    vacancy_to['building'] = i['address']['building']
                except TypeError:
                    vacancy_to['building'] = None
                vacancy_to['company_name'] = i['employer']['name']
                vacancy_to['requirement'] = i['snippet']['requirement']
                vacancy_to['responsibility'] = i['snippet']['responsibility']
                vacancy_to['experience'] = i['experience']['name']
                vacancy_to['employment'] = i['employment']['name']
                vacancy_to['schedule'] = i['schedule']['name']
                vacancy_box.append(vacancy_to)
                count += 1
            vacancies['vacancies'] = vacancy_box
            box.append(vacancies)
        return box

class DBManager():

    def __init__(self):
        pass

    @classmethod
    def create_db(cls):
        try:
            with psycopg2.connect(
                    host='localhost',
                    database='postgres',
                    user='postgres',
                    password='13799731'
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE DATABASE hh_employers')
        except psycopg2.errors.ActiveSqlTransaction:
            print('PostgreSQL не дает возможности создать БД через Python\n'
                  'Включите pgAdmin и выполнитн транзакции из файла createdb.sql')

    @classmethod
    def create_tables(cls):
        try:
            with psycopg2.connect(
                    host='localhost',
                    database='hh_employers',
                    user='postgres',
                    password='13799731'
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE TABLE employers (employer_id int PRIMARY KEY, company_name varchar(100) NOT NULL, open_vacancies int)')
                    cur.execute('CREATE TABLE vacancies (vacancy_id int PRIMARY KEY, '
                                'vacancy_name varchar(100) NOT NULL, '
                                'salary_from int, salary_to int, '
                                'salary_currency varchar(10), '
                                'city varchar(20), street varchar(20), '
                                'building varchar(10), company_name varchar(100), '
                                'requirement text, responsibility text, '
                                'experience varchar(50), '
                                'employment varchar(20), '
                                'schedule varchar(20))')
        except psycopg2.errors.DuplicateTable:
            print('Таблицы уже созданы')

    @classmethod
    def enter_data(cls, data):
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                for i in data:
                    cur.execute('INSERT INTO employers(company_name, open_vacancies) VALUES (%s, %s)',
                                [i['employer']['company_name'],i['employer']['open_vacancies']])
                    for x in i['vacancies']:
                        cur.execute('INSERT INTO vacancies(vacancy_name, salary_from, salary_to, salary_currency, city, street, building, company_name, requirement, responsibility, experience, employment, schedule) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    [x['vacancy_name'], x['salary_from'],
                                     x['salary_to'], x['salary_currency'],
                                     x['city'], x['street'],
                                     x['building'], x['company_name'],
                                     x['requirement'], x['responsibility'],
                                     x['experience'], x['employment'],
                                     x['schedule']])


data = Employer_vacancies.get_vacancies(Search_employers.get_employers('Центр'))
# for i in data:
#     print(i)
DBManager.enter_data(data)