import psycopg2

class DBManager():
    """Класс для работы с БД"""

    def __init__(self):
        pass

    @classmethod
    def create_db(cls):
        """Пытается создать БД через пайтон"""
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
                  'Включите pgAdmin и выполнитн транзакцию "CREATE DATABASE hh_employers;"')

    @classmethod
    def create_tables(cls):
        """Создает таблицы в БД"""
        try:
            with psycopg2.connect(
                    host='localhost',
                    database='hh_employers',
                    user='postgres',
                    password='13799731'
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE TABLE employers (employer_id SERIAL PRIMARY KEY, company_name varchar NOT NULL, open_vacancies int)')
                    cur.execute('CREATE TABLE vacancies (vacancy_id SERIAL PRIMARY KEY, '
                                'vacancy_name varchar NOT NULL, '
                                'salary_from int, salary_to int, '
                                'salary_currency varchar(10), '
                                'city varchar, street varchar, '
                                'building varchar, company_name varchar(100), '
                                'requirement text, responsibility text, '
                                'experience varchar, '
                                'employment varchar, '
                                'schedule varchar,'
                                'url text)')
        except psycopg2.errors.DuplicateTable:
            print('Таблицы уже созданы')
        except psycopg2.OperationalError:
            print('Отсутствует БД hh_employers')

    @classmethod
    def enter_data(cls, data):
        """Ввод данных в БД"""
        """ВНИМАНИЕ, data должен быть результатом метода get_vacancies класса Employer_vacancies"""
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
                        cur.execute('INSERT INTO vacancies(vacancy_name, salary_from, salary_to, salary_currency, city, street, building, company_name, requirement, responsibility, experience, employment, schedule, url) '
                                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    [x['vacancy_name'], x['salary_from'],
                                     x['salary_to'], x['salary_currency'],
                                     x['city'], x['street'],
                                     x['building'], x['company_name'],
                                     x['requirement'], x['responsibility'],
                                     x['experience'], x['employment'],
                                     x['schedule'], x['url']])

    @classmethod
    def get_companies_and_vacancies_count(cls):
        """Возвращает список из названий компаний и кол-во открытых вакансий"""
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM employers;')
                result_before = cur.fetchall()
                result_after = []
                for i in result_before:
                    result_after.append(list(i)[1::])
                return result_after

    @classmethod
    def get_all_vacancies(cls):
        """Возвращает список всех вакансий"""
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('select company_name, vacancy_name, salary_from, salary_to, salary_currency, url from vacancies;')
                result_before = cur.fetchall()
                result_after = []
                for i in result_before:
                    i = list(i)
                    salary = [i[2], i[3], i[4]]
                    if salary[0] == None:
                        salary[0] = '(Не указано)'
                    if salary[1] == None:
                        salary[1] = '(Не указано)'
                    if salary[2] == None:
                        salary[2] = ''
                    i.pop(2)
                    i.pop(2)
                    i.pop(2)
                    i.insert(2, f'От {salary[0]} до {salary[1]} {salary[2]}')
                    result_after.append(i)
                return result_after

    @classmethod
    def get_avg_salary(cls):
        """Возвращает среднюю зарплату"""
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("select avg(salary_to) + avg(salary_from) from vacancies where salary_currency = 'RUR'")
                result_before = cur.fetchall()
                result_after = f'Средняя зарплата - {round(list(result_before[0])[0]/2)} Рублей'
                return result_after

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        """Возвращает вакансии с повышенной зарплатой"""
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("select * from vacancies where salary_currency = 'RUR' and salary_from > (select AVG(salary_from) from vacancies)")
                result_before = cur.fetchall()
                result_after = []
                for i in result_before:
                    i = list(i)
                    i.pop(0)
                    result_after.append(i)
                return result_after

    @classmethod
    def get_vacancies_with_keyword(cls, keyword=str):
        """Возвращает вакансии по ключевым словам"""
        with psycopg2.connect(
                host='localhost',
                database='hh_employers',
                user='postgres',
                password='13799731'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("select * from vacancies "
                            f"where requirement LIKE ANY (array['%{keyword}%']) "
                            f"or vacancy_name LIKE ANY (array['%{keyword}%']) "
                            f"or responsibility LIKE ANY (array['%{keyword}%'])")
                result_before = cur.fetchall()
                result_after = []
                for i in result_before:
                    i = list(i)
                    i.pop(0)
                    result_after.append(i)
                return result_after