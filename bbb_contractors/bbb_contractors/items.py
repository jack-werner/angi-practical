# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BbbContractorsItem(scrapy.Item):
    # required fields
    company_name = scrapy.Field()
    phone_number = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    company_website_url = scrapy.Field()
    email_address = scrapy.Field()
    bbb_rating = scrapy.Field()
    accredited_date = scrapy.Field()
    profile_page_url = scrapy.Field()

    # additional fields
    company_types = scrapy.Field()
    customer_rating_avg = scrapy.Field()
    customer_review_count = scrapy.Field()
    business_start_date = scrapy.Field()
    complaints_l12m = scrapy.Field()
    complaints_l36m = scrapy.Field()
    full_address = scrapy.Field()
