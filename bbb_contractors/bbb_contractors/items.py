# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BbbContractorsItem(scrapy.Item):
    company_name = scrapy.Field()
    phone_number = scrapy.Field()
    street_address = scrapy.Field()
    city_state = scrapy.Field()
    zip_code = scrapy.Field()
    company_website_url = scrapy.Field()
    email_address = scrapy.Field()
    bbb_rating = scrapy.Field()
    accredited_date = scrapy.Field()
    profile_page_url = scrapy.Field()
    url = scrapy.Field()
