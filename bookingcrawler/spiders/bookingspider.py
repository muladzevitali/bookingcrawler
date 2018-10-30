from scrapy.spiders import Spider

from bookingcrawler.items import *
from bookingcrawler.utils import *


class BookingSpider(Spider):
    name = "booking"
    allowed_domains = ["www.booking.com"]
    domain_root = 'https://www.booking.com'.strip()

    def start_requests(self):
        cities = load_cities()

        start_urls = [(city_url.format(city), city) for city in cities]
        for (url, city) in start_urls:

            yield scrapy.Request(url,
                                 self.parse,
                                 meta={'city': city})

    def parse(self, response):
        city = response.meta.get('city')
        offset = response.xpath('//*[@id="search_results_table"]/div[4]/div[1]/ul/li[2]/ul//a/@href').extract()[-1]
        next_page_url = response.xpath(
            '//*[@id="search_results_table"]/div[4]/div[1]/ul/li[2]/ul/li[2]/a/@href').extract_first().strip()[:-2]

        number_of_rows = response.xpath('//*[@id="search_results_table"]/div[4]/div[2]/span/text()').extract_first()
        number_of_rows = int(number_of_rows.split('–')[-1].strip())

        offset = int(offset.split('offset=')[-1])
        _counter = 0

        while _counter < offset + number_of_rows:
            _page_url = next_page_url + str(_counter)

            _counter += number_of_rows
            yield scrapy.Request(_page_url,
                                 self.parse_page,
                                 meta={'city': city})

    def parse_page(self, response):

        _hotels = response.xpath('//*[@id="hotellist_inner"]/div[@data-hotelid]')

        for _hotel in _hotels:
            _hotel_stars = _hotel.xpath('./@data-class').extract_first()
            _hotel_score = _hotel.xpath('./@data-score').extract_first()
            _hotel_coordinates = _hotel.xpath('.//a[@data-coords]/@data-coords').extract_first()
            _hotel_link = _hotel.xpath('.//a[@class="hotel_name_link url"]/@href').extract_first()
            # print(_hotel_stars, _hotel_score, _hotel_coordinates, _hotel_link, '*'*100)
            hotel_link = self.domain_root + _hotel_link.strip()
            yield scrapy.Request(hotel_link,
                                 self.parse_hotel,
                                 meta={'city': response.meta.get('city'),
                                       'stars': _hotel_stars,
                                       'score': _hotel_score,
                                       'coordinates': _hotel_coordinates})

    @staticmethod
    def parse_hotel(response):
        hotel_address = response.xpath('//*[@id="showMap2"]/span[@data-bbox]/text()').extract_first().strip()
        hotel_name = response.xpath('//*[@id="hp_hotel_name"]/text()').extract_first()
        hotel_bbox_string = response.xpath('//*[@id="showMap2"]/span[2]/@data-bbox').extract_first()
        hotel_coordinates_string = response.meta.get('coordinates')

        hotel = BookingHotel()
        hotel['hotel_name'] = hotel_name.strip()
        hotel['hotel_address'] = hotel_address.strip()
        hotel['hotel_city'] = response.meta.get('city').strip()
        hotel['hotel_star'] = response.meta.get('stars').strip()
        hotel['hotel_score'] = response.meta.get('score').strip()
        hotel['hotel_coordinates'] = rotate_coordinates(hotel_coordinates_string)
        hotel['hotel_bbox'] = rotate_bbox(hotel_bbox_string)
        yield hotel
