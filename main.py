import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

base_url = 'https://dom.mingkh.ru'


def table(url):
    data = requests.get(url).text
    soup = bs(data, "html.parser")
    # table_a = soup.find_all('table')[0]

    # table = (str(table_a))
    # dfs = pd.read_html(table)

    # res = requests.get(url)
    # soup = bs(res.content,'lxml')
    
    # table = soup.select(".main-block .container .table-responsive #grid-data")
    table = soup.find_all('table')[0]
    # df = pd.read_html(str(table))
    # print(df[0].to_json(orient='records'))

    a=1

    return 1

def get_region_data(url):
    data = requests.get(url).text
    soup = bs(data, "html.parser")
    
    cities_dict = dict()
    cities = soup.select(".main-block .row .col-md-3 li a")

    for city in cities:
        cities_dict[city.text] = city['href']

    return cities_dict


def get_regions(base_url):
    data = requests.get(base_url).text
    soup = bs(data, "html.parser")

    regions_dict = dict()
    regions = soup.select(".main-block .col-md-3 a")

    for region in regions:
        regions_dict[region.text] = region['href']

    return regions_dict


def main(base_url):
    # all_regions = get_regions(base_url)
    adygeya = '/adygeya/'
    maykop = '/adygeya/maykop/'
    url = base_url + maykop
    # get_region_data(url)
    print(table(url))


if __name__ == "__main__":
    main(base_url)