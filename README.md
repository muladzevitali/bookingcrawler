# Booking.com crawler for hotels

## Running guide
* run 'git clone https://github.com/muladzevitali/bookingcrawler.git'
* run 'cd bookingcrawler'
* Insert city names in cities.txt file
* run 'scrapy runspider bookingcrawler/spiders/bookingspider.py -o results.csv'


**_column names: hotel_name, hotel_star, hotel_score, hotel_address, hotel_city, hotel_coordinates, hotel_bbox_**