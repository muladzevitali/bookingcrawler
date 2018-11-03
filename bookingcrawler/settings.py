BOT_NAME = 'bookingcrawler'

SPIDER_MODULES = ['bookingcrawler.spiders']
NEWSPIDER_MODULE = 'bookingcrawler.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
ROBOTSTXT_OBEY = True
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 7
REDIRECT_MAX_TIMES = 100
HTTPCACHE_DIR = 'httpcache'
