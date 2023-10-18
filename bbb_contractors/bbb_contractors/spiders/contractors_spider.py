import random
from pathlib import Path
from typing import Any, Iterable

import scrapy
from scrapy.http import Request, Response

class ContractorItem(scrapy.Item):
    company_name = scrapy.Field()
    phone_number = scrapy.Field()
    bbb_rating = scrapy.Field()
    profile_page_url = scrapy.Field()

class ContractorsSpider(scrapy.Spider):

    name = "roofing"

    def get_contractor(self, item):
        """
        Company name X
        Phone number X
        Address with street, city, state, and zip code
        Company Website (if available) - this might have to be found by going to profile page
        Email Address (if available)
        BBB Rating X
        Accredited Date (if available)
        Profile page URL X
        (Any other information you think is good to have/relevant)
        """
        name_xpath = ".//div/h3/a/span/text()"
        rating_xpath = ".//div/div/span/text()[3]"
        phone_xpath = './/a[contains(@href, "tel:")]/text()'
        profile_url_xpath = ".//div/h3/a/@href"

        contractor = ContractorItem()
        contractor["company_name"] = item.xpath(name_xpath).get()
        contractor["phone_number"] = item.xpath(phone_xpath).get(),
        contractor["bbb_rating"] = item.xpath(rating_xpath).get(),
        contractor["profile_page_url"] = item.xpath(profile_url_xpath).get()

        return contractor


    def start_requests(self) -> Iterable[Request]:
        bbb_url = "https://www.bbb.org/search?find_country=USA&find_entity=10126-000&find_id=1362_3100-14100&find_latlng=32.834605%2C-83.651801&find_loc=Macon%2C%20GA&find_text=Roofing%20Contractors&find_type=Category&page=1&sort=Distance"

        urls = [
            bbb_url
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response: Response) -> Any:
        results_x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div/*'
        search_results = response.xpath(results_x_path)

        self.log(f"NUMBER OF ITEMS: {len(search_results)}")
        
        for item in search_results:
            contractor = self.get_contractor(item)
            yield contractor
    
    
    