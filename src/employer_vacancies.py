import requests
import json

class Employer_vacancies():

    def __init__(self):
        pass

    """Возвращает список вакансий работодателей"""
    """employers_list должен быть результатом метода get_employers из класса Search_employers"""
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
                vacancy_to['url'] = i['alternate_url']
                vacancy_box.append(vacancy_to)
                count += 1
            vacancies['vacancies'] = vacancy_box
            box.append(vacancies)
        return box