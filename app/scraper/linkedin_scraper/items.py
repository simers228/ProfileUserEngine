# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class LinkedinItem(scrapy.Item):
    '''
    define the fields for your item here like:
    name = scrapy.Field()
    '''
    # Define our fields
    profile = Field()
    url = Field()
    about = Field()
    location = Field()
    education = Field()
    firstName = Field()
    lastName = Field()

    pass