import csv
import scrapy
from scrapy.spiders import Spider
from utils.crawler_utils import *


class BookingSpider(Spider):
    name = "booking"
    allowed_domains = ["www.booking.com"]
    hotels_dict = dict()
    domain_root = 'https://www.booking.com'
    fieldnames = ['city', 'name', 'star', 'property_type', 'district', 'address', 'languages',
                  'bbox', 'coordinates']

    def start_requests(self):
        """
        Load files to write crawled hotels, and start crawling for each city
        """
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
        """
        Generate pages for each hotel
        """
        city = response.meta.get('city')
        number_of_rows = response.xpath('//*[@id="search_results_table"]/div[4]/div[2]/span/text()').extract_first()
        number_of_rows = int(number_of_rows.split('–')[-1].strip())
        offset = get_number_of_hotels(response)
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
        """
        Parse the hotels page
        """
        _hotels = response.xpath('//*[@id="hotellist_inner"]/div[@data-hotelid]')
        for _hotel in _hotels:
            hotel_id = _hotel.xpath('./@data-hotelid').extract_first().strip()
            if self.hotels_dict.get(hotel_id):
                return None

            self.hotels_dict[hotel_id] = 1
            _hotel_district = get_district(_hotel)
            _hotel_stars = _hotel.xpath('./@data-class').extract_first()
            _hotel_coordinates = _hotel.xpath('.//a[@data-coords]/@data-coords').extract_first()
            _hotel_link = _hotel.xpath('.//div[@class="sr_item_photo"]/a/@href').extract_first()
            hotel_link = self.domain_root + _hotel_link.strip()

            yield scrapy.Request(hotel_link,
                                 self.parse_hotel,
                                 dont_filter=True,
                                 meta={'city': response.meta.get('city'),
                                       'stars': _hotel_stars,
                                       'coordinates': _hotel_coordinates,
                                       'district': _hotel_district,
                                       'writer': response.meta.get('writer')
                                       })

    @staticmethod
    def parse_hotel(response):
        """
        Parse the hotel page
        """
        hotel_address = response.xpath('//*[@id="showMap2"]/span[@data-bbox]/text()').extract_first().strip()
        hotel_name = response.xpath('//*[@id="hp_hotel_name"]/text()').extract_first()
        hotel_bbox_string = get_bbox(response)
        hotel_coordinates_string = response.meta.get('coordinates')

        writer = response.meta.get('writer')
        row = {'name': hotel_name.strip(),
               'address': hotel_address.strip(),
               'city': response.meta.get('city').strip(),
               'star': response.meta.get('stars').strip(),
               'coordinates': rotate_coordinates(hotel_coordinates_string),
               'bbox': rotate_bbox(hotel_bbox_string),
               'district': response.meta.get('district'),
               'languages': get_languages(response),
               'property_type': get_property_type(response)}
        writer.writerow(row)
