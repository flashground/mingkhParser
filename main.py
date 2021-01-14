from scraping import scraping, get_houses_csv
from pyfiglet import Figlet
import math


from utils import get_html

base_url = 'https://dom.mingkh.ru'

SCREEN_ITEMS = 8

FORMATS_TO_SAVE = ({'name': 'csv', 'ext': '.csv', 'method': 'to_csv', 'active': True},
                   {'name': 'excel', 'ext': '.xlsx', 'method': 'to_excel', 'active': True},
                   {'name': 'json', 'ext': '.json', 'method': 'to_json', 'active': False},)


def format_to_save():
    formats = []
    for index, item in enumerate(FORMATS_TO_SAVE, start=1):
        if item['active']:
            formats.append(f"{index} - {item['name']}")
    while True:
        print("В какой формате сохранить файл?")
        print(', '.join(formats))
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if choice > 0 and choice <= len(formats):
                return FORMATS_TO_SAVE[choice-1]


def show_items(url, num_to_show):
    data = scraping(get_html(url))
    screen_data = []
    for item in data:
        index = item['index']
        screen_data.append(f"{index} - {item['name']}")
        if index % num_to_show == 0 or index == len(data):
            print(', '.join(screen_data))
            screen_data.clear()
            print(f"Страница {math.ceil(index / num_to_show)} из {math.ceil(len(data) / num_to_show)}")
            print("Укажите номер или нажмите Enter для продолжения списка")
            input_num = input()
            if not input_num.isdigit():
                continue
            input_num = int(input_num)
            if input_num > 0 and input_num <= index:
                return next(i for i in data if i["index"] == input_num)
            else:
                continue


def main():
    welcome_text = Figlet(font='banner')
    print(welcome_text.renderText('HousesParser'))
    print('Показать список регионов? y/n')
    x = input()
    if x.lower() == 'y':
        region = show_items(base_url, SCREEN_ITEMS)
        region_url = f"{base_url}{region['url']}"

        locality = show_items(region_url, SCREEN_ITEMS)
        locality_url = f"{base_url}{locality['url']}houses"

        get_houses_csv(request=get_html(locality_url), url=locality_url,
                       fileformat=format_to_save(), filename=None)
        # locality_houses = get_houses_csv(houses_url)


if __name__ == "__main__":
    main()
