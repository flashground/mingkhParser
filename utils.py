import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from random import choice
import json
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def str_to_int(string):
    if not str.isdigit():
        return 0
    return int(string)


def json_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_html(url, proxy=None):
    if proxy:
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
