import csv

from scrapy.spiders import Spider

from bookingcrawler.items import *
from bookingcrawler.utils import *

links = open('links.txt', 'a')


class BookingSpider(Spider):
    name = "booking"
    allowed_domains = ["www.booking.com"]
    hotels_dict = dict()
    domain_root = 'https://www.booking.com'
    fieldnames = ['hotel_city', 'hotel_name', 'hotel_star', 'hotel_score', 'hotel_address', 'hotel_languages',
                  'hotel_bbox', 'hotel_coordinates']

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
                                 dont_filter=True,
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
        while _counter < offset + number_of_rows:
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
            hotel_id = _hotel.xpath('./@data-hotelid').extract_first().strip()
            if self.hotels_dict.get(hotel_id):
                return None

            self.hotels_dict[hotel_id] = 1

            _hotel_stars = _hotel.xpath('./@data-class').extract_first()
            _hotel_score = _hotel.xpath('./@data-score').extract_first()
            _hotel_coordinates = _hotel.xpath('.//a[@data-coords]/@data-coords').extract_first()
            _hotel_link = _hotel.xpath('.//a[@class="hotel_name_link url"]/@href').extract_first()
            hotel_link = self.domain_root + _hotel_link.strip()

            yield scrapy.Request(hotel_link,
                                 self.parse_hotel,
                                 dont_filter=True,
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
               'hotel_bbox': rotate_bbox(hotel_bbox_string),
               'hotel_languages': self.get_languages(response)}
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

    @staticmethod
    def get_clean_result(response, _xpath):
        value = response.xpath(_xpath).extract_first()
        if value:
            return value.strip()
        return None

    @staticmethod
    def get_languages(response):
        languages_list = None

        for div in response.xpath('//*[@id="hp_facilities_box"]/div[4]/div'):
            text = div.xpath('.//h5/text()').extract()
            for each in text:
                if each.strip() == 'Languages spoken':
                    languages_list = div.xpath('.//ul//text()').extract()

        if not languages_list:
            return None

        languages = [each.strip() for each in languages_list if each.strip()]
        return ', '.join(languages)
