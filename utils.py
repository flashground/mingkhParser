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
