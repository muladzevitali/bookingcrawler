def load_cities():
    with open('cities.txt', 'r') as _input_file:
        cities = _input_file.readlines()

    cities = [city.strip() for city in cities]

    return cities


city_url = 'http://www.booking.com/searchresults.html?src=index&nflt=&error_url=http%3A%2F%2F' \
           'www.booking.com%2Findex.en-gb.html%3Fsid%3Debf463cfc313cfe4089c1cef5d42de23%3Bdc' \
           'id%3D1%3B&dcid=1&lang=en-gb&sid=ebf463cfc313cfe4089c1cef5d42de23&si=ai%2Cco%2Cci%2' \
           'Cre%2Cdi&dest_type_filter=all&ss={}&checkin_monthday=0&checkin_year_month=0&' \
           'checkout_monthday=0&checkout_year_month=0&idf=on&org_nr_rooms=1&org_nr_adults=2&org_nr_children=0'


city_url_pages = 'https://www.booking.com/searchresults.html?aid=304142&label' \
                 '=gen173nr-1DCAQoggJCDnNlYXJjaF90YmlsaXNpSAlYBGhSiAEBmAEuwgEDeDExy' \
                 'AEM2AED6AEB-AEIkgIBeagCAw&sid=19a70cb1bcb0923e1c2ed58f029a48c7&tmpl=' \
                 'searchresults&class_interval=1&dest_id=900047975&dest_type=city&dtdisc=' \
                 '0&group_adults=2&group_children=0&idf=1&inac=0&index_postcard=0&label_click' \
                 '=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total' \
                 '&si=ai%2Cco%2Cci%2Cre%2Cdi&src=index&ss={}&ss_all=0&ssb=empty&sshis=0&rows=50&offset={}'

cities_url = [city_url.format(city) for city in load_cities()]

city_url_mapper = {city_url.format(city): city_url_pages.format(city, 100) for city in load_cities()}
