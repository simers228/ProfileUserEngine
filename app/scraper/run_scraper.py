from .linkedin_scraper.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .linkedin_scraper import settings
import os

class ScraperClass:
    def __init__(self):
        #settings_file_path = 'scraper.scraper.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = LinkedInPeopleProfileSpider # The spider you want to crawl

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()