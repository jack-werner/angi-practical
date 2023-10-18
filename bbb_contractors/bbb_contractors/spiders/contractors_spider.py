from pathlib import Path
from typing import Any, Iterable

import scrapy
from scrapy.http import Request, Response

class ContractorsSpider(scrapy.Spider):

    name = "roofing"

    def start_requests(self) -> Iterable[Request]:
        bbb_url = "https://www.bbb.org/search?find_country=USA&find_entity=10126-000&find_id=1362_3100-14100&find_latlng=32.834605%2C-83.651801&find_loc=Macon%2C%20GA&find_text=Roofing%20Contractors&find_type=Category&page=1&sort=Distance"
        # bbb_url = "https://www.bbb.org/"

        urls = [
            bbb_url
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response: Response) -> Any:
        x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[4]'
        item = response.xpath(x_path)
        
        print(f"XPath Item:{item}")
        self.log(f"XPath Item:{item}")
        filename = "contractor.html"
        Path(filename).write_bytes(response.body)
    
    