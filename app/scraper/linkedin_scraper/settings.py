from . import spiders
from . import pipelines

def get_full_package_name_for_class(clazz) -> str:
    return ".".join([clazz.__module__, clazz.__name__])

BOT_NAME = 'linkedin_people_profile'

SPIDER_MODULES = [spiders.__name__]
NEWSPIDER_MODULE = spiders.__name__


# HTTPCACHE_ENABLED = True

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}


DOWNLOADER_MIDDLEWARES = {

    # ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,

    # Proxy Middleware
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 30
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_DELAY = 0.2
DNSCACHE_SIZE = 20000

# Activate pipelines to connect to SQL Database
ITEM_PIPELINES = {
    get_full_package_name_for_class(pipelines.LinkedinPipeline): 300,
}
