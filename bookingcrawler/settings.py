BOT_NAME = 'bookingcrawler'

SPIDER_MODULES = ['bookingcrawler.spiders']
NEWSPIDER_MODULE = 'bookingcrawler.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
ROBOTSTXT_OBEY = True
# DOWNLOAD_DELAY = 3
HTTPCACHE_ENABLED = True
# COOKIES_ENABLED = True
# COOKIES_DEBUG = True
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 7
REDIRECT_MAX_TIMES = 100
# REDIRECT_ENABLE = False
HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
