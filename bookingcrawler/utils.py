

city_url = 'http://www.booking.com/searchresults.html?src=index&nflt=&error_url=http%3A%2F%2F' \
           'www.booking.com%2Findex.en-gb.html%3Fsid%3Debf463cfc313cfe4089c1cef5d42de23%3Bdc' \
           'id%3D1%3B&dcid=1&lang=en-gb&sid=ebf463cfc313cfe4089c1cef5d42de23&si=ai%2Cco%2Cci%2' \
           'Cre%2Cdi&dest_type_filter=all&ss={}&checkin_monthday=0&checkin_year_month=0&' \
           'checkout_monthday=0&checkout_year_month=0&idf=on&org_nr_rooms=1&org_nr_adults=2&org_nr_children=0'


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
