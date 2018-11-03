import requests
import scrapy

head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

city_url = 'https://www.booking.com/hotel/ge/tbilisi-marriott.en-gb.html#basiclayout'
response = requests.get(city_url, headers=head)
tree = scrapy.Selector(response)
script = tree.xpath('//*[@data-bbox]/@data-bbox').extract()
print(response.url, script)
