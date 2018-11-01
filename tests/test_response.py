import requests
import scrapy

city_name = 'vegas'
city_url = 'https://www.booking.com/hotel/ru/apartamienty-na-tvierskoi.en-gb.html?aid=304142;label=gen173nr-1DCAQoggJCDnNlYXJjaF90YmlsaXNpSAlYBGhSiAEBmAEuwgEDeDExyAEM2AED6AEB-AEDkgIBeagCAw;sid=19a70cb1bcb0923e1c2ed58f029a48c7;dest_id=-2960561;dest_type=city;dist=0;hapos=1;hpos=1;room1=A%2CA;sb_price_type=total;srepoch=1541087141;srfid=edf8cef3e9d126bee669694dde8674fc0c292121X1;srpvid=a3546ed2ee850032;type=total;ucfs=1&#hotelTmpl'

response = requests.get(city_url)
tree = scrapy.Selector(response)
languages_list = None
for div in tree.xpath('//*[@id="hp_facilities_box"]/div[4]/div'):
    text = div.xpath('.//h5/text()').extract()
    print(text)
    for each in text:
        if each.strip() == 'Languages spoken':
            print('here')
            languages_list = div.xpath('.//ul//text()').extract()

print(languages_list)
