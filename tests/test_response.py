import requests


city_name = 'vegas'
city_url = f'http://www.booking.com/searchresults.html?src=index&nflt=&error_url=' \
           f'http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Fsid%3Debf463cfc313cfe' \
           f'4089c1cef5d42de23%3Bdcid%3D1%3B&dcid=1&lang=en-gb&sid=ebf463cfc313cfe4089c1ce' \
           f'f5d42de23&si=ai%2Cco%2Cci%2Cre%2Cdi&dest_type_filter=all&ss={city_name}' \
           f'&checkin_monthday=0&checkin_year_month=0&checkout_monthday=0&checkout_year_month=0' \
           f'&idf=on&org_nr_rooms=1&org_nr_adults=2&org_nr_children=0'

print(city_url)
response = requests.get(city_url)

# 'https://www.booking.com/searchresults.en-gb.html?si=ai%2Cco%2Cci%2Cre%2Cdi;ss=new%20york'