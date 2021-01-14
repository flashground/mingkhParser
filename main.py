import sys
import math

import settings
from utils import get_html, welcome_text, format_to_save
from scraping import scraping, get_houses_csv


def show_items(url, num_to_show):
    data = scraping(get_html(url))
    screen_data = []
    for num, item in enumerate(data):
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
            if input_num in range(1, index+1):
                return next(i for i in data if i["index"] == input_num)
            elif num+1 == len(data):
                sys.exit()
            else:
                continue



def main():
    print(welcome_text(settings.WELCOME_TEXT))
    print('Показать список регионов? y/n')
    answer = input()
    if answer.lower() == 'y':
        region = show_items(settings.BASE_URL, settings.SCREEN_ITEMS)
        region_url = f"{settings.BASE_URL}{region['url']}"

        locality = show_items(region_url, settings.SCREEN_ITEMS)
        locality_url = f"{settings.BASE_URL}{locality['url']}houses"

        get_houses_csv(request=get_html(locality_url), url=locality_url,
                       fileformat=format_to_save(), filename=None)
        # locality_houses = get_houses_csv(houses_url)


if __name__ == "__main__":
    main()
