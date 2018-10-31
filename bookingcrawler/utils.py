
city_url = 'https://www.booking.com/searchresults.en-gb.html?ss={}&order=class'

first_page = 'http://www.booking.com/searchresults.en-gb.html?si=ai%2Cco%2Cci%2Cre%2Cdi;ss={}&order=class'
print(first_page.format('moscow'))


def load_cities():
    with open('cities.txt', 'r') as _input_file:
        cities = _input_file.readlines()

    cities = [city.strip() for city in cities]

    return cities


def rotate_coordinates(_coordinates):
    if not _coordinates:
        return None
    y, x = _coordinates.strip().split(',')
    return float(x), float(y)


def rotate_bbox(bbox):
    if not bbox:
        return None
    y0, x0, y1, x1 = bbox.strip().split(',')
    return [(x0, y0), (x1, y1)]
