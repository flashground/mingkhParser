import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import time
from bs4 import BeautifulSoup
from random import choice
from pyfiglet import Figlet
import settings

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def welcome_text(text):
    """
    Формирование ASCll псевдографики из заданного текста.
    """
    figlet = Figlet(font='banner')
    return figlet.renderText(text)


def str_to_int(string):
    """
    Проверка строки на возможность преобразования в число.
    """
    if not str.isdigit():
        return 0
    return int(string)


def format_to_save():
    """
    Функция выбора формата для сохранения данных.
    """
    formats = []
    for index, item in enumerate(settings.FORMATS_TO_SAVE, start=1):
        if item['active']:
            formats.append(f"{index} - {item['name']}")
    while True:
        print("В какой формате сохранить файл?")
        print(', '.join(formats))
        answer = input()
        if answer.isdigit():
            answer = int(answer)
            if answer in range(len(formats)+1):
                return settings.FORMATS_TO_SAVE[answer-1]


def json_to_file(filename, data):
    """
    Функция сохранения JSON данных в файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_html(url, proxy=None):
    """
    Функция подключения к серверу и сбора html.
    """
    if settings.PROXY:
        p = get_proxy()
        proxy = {p['schema']: p['address']}
    x = 0
    while x < 5:
        x += 1
        try:
            r = requests.get(url, proxies=proxy, timeout=5, verify=False)
            return r.text
        except requests.exceptions.ReadTimeout:
            print("\n Переподключение к серверу \n")
            time.sleep(3)


def get_proxy():
    """
    Функция парсинга прокси серверов с ресурса https://free-proxy-list.net/ и выдача случайного.
    """
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)
    return choice(proxies)


def pagination_check(soup):
    """
        Проверка наличия пагинации на странице (многостраничная таблица).
        Вывод - число страниц (n или 1 если пагинации нет)
    """
    pagination = soup.find('ul', attrs={'class': 'pagination'})
    if pagination:
        last_page_url = pagination.find_all('li')[-1].a['href']
        pages = last_page_url.split("=")[-1]
        if pages.isdigit():
            return int(pages)
        return 1
    return 1
