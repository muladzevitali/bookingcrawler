import scrapy


class BookingCity(scrapy.Item):
    apartments = scrapy.Field()
    hotels = scrapy.Field()
    guest_houses = scrapy.Field()
    hostels = scrapy.Field()
    holiday_homes = scrapy.Field()
    homestays = scrapy.Field()
    bed_and_breakfasts = scrapy.Field()
    villas = scrapy.Field()
    economy_hotels = scrapy.Field()
    country_houses = scrapy.Field()
    lodges = scrapy.Field()
    motels = scrapy.Field()
    lampsites = scrapy.Field()
    chalets = scrapy.Field()
    love_hotels = scrapy.Field()
    resorts = scrapy.Field()
    farm_stays = scrapy.Field()
    luxury_tents = scrapy.Field()
    holiday_parks = scrapy.Field()
    riads = scrapy.Field()


class BookingHotel(scrapy.Item):
    hotel_name = scrapy.Field()
    hotel_star = scrapy.Field()
    hotel_score = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_city = scrapy.Field()
    hotel_coordinates = scrapy.Field()
    hotel_bbox = scrapy.Field()






