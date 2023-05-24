import scrapy
from RecruiterAI.linkedin.items import LinkedinItem


class LinkedinSpider(scrapy.Spider):
    name = 'seq_app'

    def start_requests(self):
        url = 'some url'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # rename based on what we're actually calling
        tbl_linkedin_object = LinkedinItem()
        for quote in response.css('div.quote'):
            tbl_linkedin_object['profile'] = quote.css('span.text::text').get()

            '''
            some code for the rest of the variables
            '''
            yield tbl_linkedin_object
