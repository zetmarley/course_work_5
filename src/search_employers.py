from src.HH_API import HH_API
import requests
import json

class Search_employers():
    """Класс для поиска работодателей"""
    def __init__(self):
        pass

    """Возвращает список работодателей"""
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