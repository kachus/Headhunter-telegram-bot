import requests
import json
import json
import logging
from datetime import date, timedelta


from bs4 import BeautifulSoup


def remove_tags(string):
    markup = string
    soup = BeautifulSoup(markup, 'html.parser')
    return soup.get_text()

def get_key_words() -> str:
    with open("/Users/Evgenia/Desktop/keywords.txt", 'r') as f:
        for line in f:
            keywords = line.strip()
        return str(keywords)

def get_daterange():
    date_to = date.today()
    with open("/Users/Evgenia/Desktop/date_range.txt", 'r') as f:
        for line in f:
            daterange = line.strip()
        if daterange == '2 weeks':
            delta = 14
        elif daterange == '1 week':
            delta = 7
        elif daterange == '1 day':
            delta = 1
        try:
            date_from = date_to -  timedelta(days=delta)
        except:
            raise ValueError ('No value for delta')
        return str(date_from), str(date_to)



def get_vacancies()  -> list:
    url = 'https://api.hh.ru/vacancies'
    query = {'text': get_key_words(),
             'area': {'1', '2'},
             'only_with_salary': 'true',
             'date_from': get_daterange()[0],
             'date_to': get_daterange()[1],
             'per_page': '20',
             'schedule': 'remote'
             }
    response = requests.get((url), params=query)
    json_response= response.json()
    list_vacancies = json_response['items']
    answers = []
    for vacancy in list_vacancies:
        vacancy_name = vacancy['name']
        city = vacancy['area']['name']
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        url = vacancy['alternate_url']
        requirement = remove_tags(vacancy['snippet']['requirement'])
        responsibility = remove_tags(vacancy['snippet']['responsibility'])
        employer_name = vacancy['employer']['name']
        employer_link = vacancy['employer']['alternate_url']
        answer = f'Bакансия: {vacancy_name} ' \
                 f'\n Работодатель: {employer_name}' \
                 f' \n Требования: {requirement}' \
                 f' \n Зп от: {salary_from} \n Зп до: {salary_to}' \
                 f'\n Обязанности: {responsibility}' \
                 f'\n Ссылка на вакансию: {url}' \
                 f'\n Ссылка на работодателя: {employer_link}'
        '''answer = {'Работодатель': employer_name, 'Вакансия': vacancy_name, 'Зп от': salary_from, 'До': salary_to, 'Город': city, 'Ссылка на вакансию:': url,
              'Требования': requirement, 'Обязанности' : responsibility, 'Ссылка на работодателя': employer_link}'''
        answers.append(answer)

    return answers
    #return json.dumps(answer, ensure_ascii=False)
