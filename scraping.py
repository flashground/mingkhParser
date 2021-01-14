from bs4 import BeautifulSoup as bs
from unicodedata import normalize
import pandas as pd

from utils import pagination_check, json_to_file


def scraping(request):
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
    soup = bs(request, "lxml")

    all_data = []
    data = soup.select(".main-block .row .col-md-3 li a")

    for index, item in enumerate(data, start=1):
        all_data.append({'index': index,
                         'name': normalize('NFKD', item.text),
                         'url': item['href']})
    return all_data


def get_houses_csv(request, url, fileformat, filename=None):
    """
        Парсинг всех домов и сохранение в файл.
    """
    if not filename:
        filename = f"{url.split('/')[-2]}{fileformat['ext']}"
    else:
        filename = f"{filename}{fileformat['ext']}"

    soup = bs(request, "html.parser")
    pages = pagination_check(soup)

    df_list = []
    for x in range(1, pages+1):
        page_url = f"{url}?page={x}"
        df_list.append(pd.read_html(page_url)[0])
    data = pd.concat(df_list, join='inner')
    method_to_call = getattr(data, fileformat['method'])

    if fileformat['name'] == 'json':
        json_to_file(filename, method_to_call(orient='records', force_ascii=False))
    elif fileformat['name'] in ['csv', 'excel']:
        method_to_call(filename, index=False)
    else:
        pass
    print(f"Файл сохранен с именем {filename}")
