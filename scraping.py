import requests
from bs4 import BeautifulSoup as bs
from unicodedata import normalize
import pandas as pd

from utils import pagination_check


def scrapping(url):
    """
        Парсинг регионов, населенныхх пунктов или городов.
        Формат вывода:
        [
           {
              "index":1,
              "name":"Адыгея",
              "url":"/adygeya/"
           }
        ]
    """
    data = requests.get(url).text
    soup = bs(data, "html.parser")

    all_data = []
    data = soup.select(".main-block .row .col-md-3 li a")

    for index, item in enumerate(data, start=1):
        all_data.append({'index': index,
                         'name': normalize('NFKD', item.text),
                         'url': item['href']})
    return all_data


def get_houses_csv(url):
    """
    Парсинг всех домов.
    Формат вывода: csv
    """
    data = requests.get(url).text
    soup = bs(data, "html.parser")
    pages = pagination_check(soup)

    df_list = []
    for x in range(1, pages+1):
        page_url = f"{url}?page={x}"
        df_list.append(pd.read_html(page_url)[0])
    data = pd.concat(df_list)
    return data.to_csv()
