from scraping import scrapping, get_houses_csv
from pyfiglet import Figlet

base_url = 'https://dom.mingkh.ru'
region_url = base_url + '/adygeya/'
city_url = region_url + 'maykop/'
streets_url = city_url + '12-marta-ulica/'
houses_url = city_url + 'houses/'


def main():
    welcome_text = Figlet(font='banner')
    print(welcome_text.renderText('HousesParser'))
    print('Показать список регионов? y/n')
    # x = input()
    # x = 'y'
    # if x.lower() == 'y':
    #     all_regions = get_regions(base_url)
    #     regions = []
    #     for region in all_regions:
    #         pass

    # all_regions = scrapping(base_url)
    # region_locality = scrapping(region_url)
    # locality_streets = scrapping(city_url)
    #
    # locality_houses = get_houses_csv(houses_url)
    # streets_houses = get_houses_csv(streets_url)


if __name__ == "__main__":
    main()
