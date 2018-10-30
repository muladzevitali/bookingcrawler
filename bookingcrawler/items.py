import scrapy


class BookingHotel(scrapy.Item):
    hotel_name = scrapy.Field()
    hotel_star = scrapy.Field()
    hotel_score = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_city = scrapy.Field()
    hotel_coordinates = scrapy.Field()
    hotel_bbox = scrapy.Field()
