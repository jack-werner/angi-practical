from pathlib import Path
from typing import Any, Iterable

import scrapy
from scrapy.http import Request, Response

class ContractorsSpider(scrapy.Spider):

    name = "roofing"

    def get_data(self ):
        """
        Company name
        Phone number
        Address with street, city, state, and zip code
        Company Website (if available)
        Email Address (if available)
        BBB Rating
        Accredited Date (if available)
        Profile page URL
        (Any other information you think is good to have/relevant)
        """

    def start_requests(self) -> Iterable[Request]:
        bbb_url = "https://www.bbb.org/search?find_country=USA&find_entity=10126-000&find_id=1362_3100-14100&find_latlng=32.834605%2C-83.651801&find_loc=Macon%2C%20GA&find_text=Roofing%20Contractors&find_type=Category&page=1&sort=Distance"

        urls = [
            bbb_url
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response: Response) -> Any:
        # x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[4]'
        results_x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div/*'
                        #  '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[4]/div/div[2]/div/div[2]/p[1]/a'
        search_results = response.xpath(results_x_path)

        self.log(f"NUMBER OF ITEMS: {len(search_results)}")
        
        for item in search_results:
            name_xpath = ".//div/h3/a/span/text()"
            # //*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[4]/div/div[2]/div/div[2]/p[1]/a
            phone_xpath = './/a[contains(@href, "tel:")]/text()'
            yield {
                "company_name": item.xpath(name_xpath).get(),
                "phone_number": item.xpath(phone_xpath).get(),
            }
        # print(f"XPath Item:{item}")
        # self.log(f"XPath Item:{item}")
        # filename = "contractor.html"
        # Path(filename).write_bytes(response.body)
    
    