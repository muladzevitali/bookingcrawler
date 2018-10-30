import requests
import scrapy
city_name = 'vegas'
city_url = 'https://www.booking.com/hotel/ge/salve-tbilisi.en-gb.html?label=gen173nr-' \
           '1DCAEoggJCAlhYSDNYBGhSiAEBmAEuwgEDeDExyAEM2AED6AEBkgIBeagCAw;sid=19a70cb1bcb092' \
           '3e1c2ed58f029a48c7;dest_id=900047975;dest_type=city;dist=0;group_adults=2;hapos=1;' \
           'hpos=1;room1=A%2CA;sb_price_type=total;srepoch=1540941367;srfid=f729acfce5459008' \
           '00ffe7853dd3690a3fb93a6dX1;srpvid=0f79a39b84ee00de;type=total;ucfs=1&#hotelTmpl'

print(city_url)
response = requests.get(city_url)
tree = scrapy.Selector(response)
bbox = tree.xpath('//*[@id="showMap2"]/span[2]/@data-bbox').extract()
print(bbox)