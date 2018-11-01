import requests
import scrapy

city_name = 'vegas'
city_url = 'http://www.booking.com/searchresults.en-gb.html?si=ai%2Cco%2Cci%2Cre%2Cdi;ss=tbilisi&order=class'
response = requests.get(city_url)
tree = scrapy.Selector(response)
script = tree.xpath('//a[@class="hotel_lp_alt_theme_links"]').extract()
print(script)
# print(response.url)
file = open("resp_text.html", "w")
file.write(response.text)
file.close()