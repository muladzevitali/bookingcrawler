from scrapy.spiders import Spider
from utils import *
from bookingcrawler.items import *


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
                                 meta={'start_url': url,
                                       'city': city})

    def parse(self, response):
        city = response.meta.get('city')
        offset = response.xpath('//*[@id="search_results_table"]/div[4]/div[1]/ul/li[2]/ul//a/@href').extract()[-1]
        offset = int(offset.split('offset=')[-1])
        _counter = 0
        while _counter < offset:

            _page_url = city_url_pages.format(city, _counter)
            _counter += 50
            yield scrapy.Request(_page_url,
                                 self.parse_page,
                                 meta={'city': city})

    def parse_page(self, response):

        _hotel_links = response.xpath('//*[@id="hotellist_inner"]/div//h3/a/@href').extract()
        for _hotel_link in _hotel_links:
            hotel_link = self.domain_root + _hotel_link.strip()
            yield scrapy.Request(hotel_link,
                                 self.parse_hotel,
                                 meta={'city': response.meta.get('city')})

    def parse_hotel(self, response):
        city = response.meta.get('city')
        address = response.xpath('//*[@id="showMap2"]/span/text()').extract_first().strip()
        print(address)