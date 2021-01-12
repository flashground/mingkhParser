import requests
from bs4 import BeautifulSoup as bs
from unicodedata import normalize
import pandas as pd


base_url = 'https://dom.mingkh.ru'
region_url = base_url + '/adygeya/'
city_url = region_url + 'maykop/'
streets_url = city_url + '12-marta-ulica/'
houses_url = city_url + 'houses/'


def pagination_check(soup):
    '''
        Проверка наличия пагинации на странице (многостраничная таблица).
        Вывод - число страниц (n или 1 если пагинации нет)
    '''
    pagination = soup.find('ul', attrs={'class': 'pagination'})
    if pagination:
        last_page_url = pagination.find_all('li')[-1].a['href']
        pages = last_page_url.split("=")[-1]
        if pages.isdigit():
            return int(pages)
        return 1
    return 1


def get_regions(base_url):
    '''
        Парсинг всех регионов.
        Формат вывода {'Адыгея':'/adygeya/','Алтай':'/altay/', ...}
    '''
    data = requests.get(base_url).text
    soup = bs(data, "html.parser")

    regions_dict = dict()
    regions = soup.select(".main-block .col-md-3 a")

    for region in regions:
        regions_dict[normalize('NFKD', region.text)] = region['href']

    return regions_dict


def get_region_locality(url):
    '''
        Парсинг всех населенных пунктов региона.
        Формат вывода {'Майкоп':'/adygeya/maykop/','Энем':'/adygeya/enem/', ...}
    '''
    data = requests.get(url).text
    soup = bs(data, "html.parser")

    cities_dict = dict()
    cities = soup.select(".main-block .row .col-md-3 li a")

    for city in cities:
        cities_dict[normalize('NFKD', city.text)] = city['href']

    return cities_dict


def get_locality_streets(url):
    '''
        Парсинг всех улиц населенного пункта.
        Формат вывода {'12 Марта улица':'/adygeya/maykop/12-marta-ulica',
                        '2-ой переулок':'/adygeya/maykop/2-y-pereulok', ...}
    '''
    data = requests.get(url).text
    soup = bs(data, "html.parser")
    
    streets_dict = dict()
    streets = soup.select(".main-block .row .col-md-3 li a")

    for street in streets:
        streets_dict[normalize('NFKD', street.text)] = street['href']

    return streets_dict


def get_streets_houses_csv(url):
    '''
        Парсинг всех домов на улице.
        Формат вывода csv
    '''
    data = pd.read_html(url)
    return data[0].to_csv()


def get_locality_houses_csv(url):
    '''
        Парсинг всех домов населенного пункта.
        Формат вывода csv
    '''
    data = requests.get(url).text
    soup = bs(data, "html.parser")
    pages = pagination_check(soup)

    df_list = []
    for x in range(1, pages+1):
        page_url = f"{url}?page={x}"
        df_list.append(pd.read_html(page_url)[0])
    data = pd.concat(df_list)
    return data.to_csv()


def main():
    all_regions = get_regions(base_url)
    region_locality = get_locality_streets(region_url)
    locality_houses = get_locality_houses_csv(houses_url)
    locality_streets = get_locality_streets(city_url)
    streets_houses = get_streets_houses_csv(streets_url)


if __name__ == "__main__":
    main()