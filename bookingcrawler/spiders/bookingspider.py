import csv

from scrapy.spiders import Spider

from bookingcrawler.items import *
from bookingcrawler.utils import *

links = open('links.txt', 'a')


class BookingSpider(Spider):
    name = "booking"
    allowed_domains = ["www.booking.com"]
    domain_root = 'https://www.booking.com'
    fieldnames = ['hotel_city', 'hotel_name', 'hotel_star', 'hotel_score', 'hotel_address', 'hotel_bbox',
                  'hotel_coordinates']

    def start_requests(self):
        cities = load_cities()
        city_writers = dict()
        for city in cities:
            file_name = open(f'results/{city}.csv', 'a')
            city_writers.update({city: csv.DictWriter(file_name, fieldnames=self.fieldnames)})

        for _, value in city_writers.items():
            value.writeheader()

        start_urls = [(city_url.format(city), city) for city in cities]
        for (url, city) in start_urls:
            yield scrapy.Request(url,
                                 self.parse,
                                 meta={'city': city,
                                       'url': url,
                                       'writer': city_writers[city]
                                       })

    def parse(self, response):
        city = response.meta.get('city')
        number_of_rows = response.xpath('//*[@id="search_results_table"]/div[4]/div[2]/span/text()').extract_first()
        number_of_rows = int(number_of_rows.split('–')[-1].strip())

        offset = self.get_number_of_hotels(response)
        _counter = 0
        while _counter < 1000:
            if _counter == 0:

                yield scrapy.Request(city_url.format(city),
                                     self.parse_page,
                                     dont_filter=True,
                                     meta={'city': city,
                                           'writer': response.meta.get('writer'),
                                           'url': 'offset_0'})
            else:
                old_offset = f'&offset={_counter}'
                _page_url = response.meta.get('url') + old_offset

                yield scrapy.Request(_page_url,
                                     self.parse_page,
                                     dont_filter=True,
                                     meta={'city': city,
                                           'writer': response.meta.get('writer'),
                                           'url': _page_url
                                           })

            _counter += number_of_rows

    def parse_page(self, response):
        _hotels = response.xpath('//*[@id="hotellist_inner"]/div[@data-hotelid]')
        for _hotel in _hotels:
            _hotel_stars = _hotel.xpath('./@data-class').extract_first()
            _hotel_score = _hotel.xpath('./@data-score').extract_first()
            _hotel_name = _hotel.xpath(
                './/span[@data-et-click]/text()').extract_first().strip()

            _hotel_coordinates = _hotel.xpath('.//a[@data-coords]/@data-coords').extract_first()
            _hotel_link = _hotel.xpath('.//a[@class="hotel_name_link url"]/@href').extract_first()
            hotel_link = self.domain_root + _hotel_link.strip()
            if response.meta.get('city') == 'Tbilisi':
                links.write(_hotel_name + ' ' + response.meta.get('url') + '\n')
                links.flush()
            yield scrapy.Request(hotel_link,
                                 self.parse_hotel,
                                 meta={'city': response.meta.get('city'),
                                       'stars': _hotel_stars,
                                       'score': _hotel_score,
                                       'coordinates': _hotel_coordinates,
                                       'writer': response.meta.get('writer')
                                       })

    def parse_hotel(self, response):
        hotel_address = response.xpath('//*[@id="showMap2"]/span[@data-bbox]/text()').extract_first().strip()
        hotel_name = response.xpath('//*[@id="hp_hotel_name"]/text()').extract_first()
        hotel_bbox_string = self.get_bbox(response)
        hotel_coordinates_string = response.meta.get('coordinates')
        writer = response.meta.get('writer')
        row = {'hotel_name': hotel_name.strip(),
               'hotel_address': hotel_address.strip(),
               'hotel_city': response.meta.get('city').strip(),
               'hotel_star': response.meta.get('stars').strip(),
               'hotel_score': response.meta.get('score').strip(),
               'hotel_coordinates': rotate_coordinates(hotel_coordinates_string),
               'hotel_bbox': rotate_bbox(hotel_bbox_string)}
        writer.writerow(row)

    @staticmethod
    def get_bbox(response):
        hotel_bbox_string = response.xpath('//*[@data-bbox]/@data-bbox').extract()
        for bbox in hotel_bbox_string:
            if bbox:
                return bbox
        return None

    @staticmethod
    def get_number_of_hotels(response):
        _header_string = response.xpath('//*[@class="sr_header--title"]//*[@class="sorth1"]/text()').extract_first()
        _numbers_string = int(list(filter(lambda x: ',' in x, _header_string.split(' ')))[0].replace(',', ''))
        return _numbers_string

    def get_property_type(self, property_type, response):
        base_xpath = '//*[@id="filter_hoteltype"]/div[2]/a[{}]//span[@class="filter_count"]/text()'
        property_type['apartments'] = self.get_clean_result(response, base_xpath.format(1))
        property_type['hotels'] = self.get_clean_result(response, base_xpath.format(2))
        property_type['guest_houses'] = self.get_clean_result(response, base_xpath.format(3))
        property_type['hostels'] = self.get_clean_result(response, base_xpath.format(4))
        property_type['holiday_homes'] = self.get_clean_result(response, base_xpath.format(5))
        property_type['homestays'] = self.get_clean_result(response, base_xpath.format(6))
        property_type['bed_and_breakfasts'] = self.get_clean_result(response, base_xpath.format(7))
        property_type['villas'] = self.get_clean_result(response, base_xpath.format(8))
        property_type['economy_hotels'] = self.get_clean_result(response, base_xpath.format(9))
        property_type['country_houses'] = self.get_clean_result(response, base_xpath.format(10))
        property_type['lodges'] = self.get_clean_result(response, base_xpath.format(11))
        property_type['motels'] = self.get_clean_result(response, base_xpath.format(12))
        property_type['lampsites'] = self.get_clean_result(response, base_xpath.format(13))
        property_type['chalets'] = self.get_clean_result(response, base_xpath.format(14))
        property_type['love_hotels'] = self.get_clean_result(response, base_xpath.format(15))
        property_type['resorts'] = self.get_clean_result(response, base_xpath.format(16))
        property_type['farm_stays'] = self.get_clean_result(response, base_xpath.format(17))
        property_type['luxury_tents'] = self.get_clean_result(response, base_xpath.format(18))
        property_type['holiday_parks'] = self.get_clean_result(response, base_xpath.format(19))
        property_type['riads'] = self.get_clean_result(response, base_xpath.format(20))

    @staticmethod
    def get_clean_result(response, _xpath):
        value = response.xpath(_xpath).extract_first()
        if value:
            return value.strip()
        return None
