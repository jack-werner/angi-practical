from typing import Any, Iterable

import scrapy
from scrapy.http import Request, Response

from bbb_contractors.items import BbbContractorsItem


class ContractorsSpider(scrapy.Spider):
    name = "roofing"
    follow = False

    def get_contractor(self, item):
        # required fields
        name_xpath = ".//div/h3/a/span/text()"
        phone_xpath = './/a[contains(@href, "tel:")]/text()'
        street_address_xpath = ".//div[2]/div/div/p[2]/text()"
        city_state_xpath = ".//div[2]/div/div/p[2]/text()[2]"
        zip_code_xpath = ".//div[2]/div/div/p[2]/span[2]/text()"
        rating_xpath = ".//div/div/span/text()[3]"
        profile_url_xpath = ".//div/h3/a/@href"
        # additional fields
        company_type_xpath = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[12]/div/div[1]/div[1]/p/text()'

        contractor = BbbContractorsItem()

        contractor["company_name"] = item.xpath(name_xpath).get()
        contractor["phone_number"] = item.xpath(phone_xpath).get()
        contractor["street_address"] = item.xpath(street_address_xpath).get()
        contractor["zip_code"] = item.xpath(zip_code_xpath).get()
        contractor["bbb_rating"] = item.xpath(rating_xpath).get()
        contractor["profile_page_url"] = item.xpath(profile_url_xpath).get()
        contractor["company_types"] = item.xpath(company_type_xpath).get()

        city_state = item.xpath(city_state_xpath).get()
        if city_state:
            city_state_list = city_state.split(",")
            city = city_state_list[0]
            state = city_state_list[1]

            contractor["city"] = city.strip()
            contractor["state"] = state.strip()

        return contractor

    def start_requests(self) -> Iterable[Request]:
        roofing_url = "https://www.bbb.org/search?find_country=USA&find_entity=10126-000&find_id=1362_3100-14100&find_latlng=32.834605%2C-83.651801&find_loc=Macon%2C%20GA&find_text=Roofing%20Contractors&find_type=Category&page=1&sort=Distance"
        urls = [roofing_url]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_contractor_profile(self, response: Response, item: BbbContractorsItem):
        # required fields
        website_xpath = "//*[text() = 'Visit Website']/@href"
        accredited_date_xpath = (
            "//*[text() = 'Accredited Since']/following-sibling::text()"
        )

        # additional fields
        customer_rating_avg_xpath = "//span[contains(text(), '/5') ]/text()"
        customer_review_count_xpath = "//p[contains(text(), 'Average of') ]/text()"
        business_start_date_xpath = (
            "//*[contains(text(), 'Business Started') ]/following-sibling::dd/text()"
        )
        complaints_l36m_xpath = "//p[contains(text(), 'last 3 years')]/strong/text()"
        complaints_l12m_xpath = "//p[contains(text(), 'last 12 months')]/strong/text()"

        item["company_website_url"] = response.xpath(website_xpath).get()
        item["accredited_date"] = response.xpath(accredited_date_xpath).get()
        item["customer_rating_avg"] = response.xpath(customer_rating_avg_xpath).get()
        item["customer_review_count"] = response.xpath(
            customer_review_count_xpath
        ).get()
        item["business_start_date"] = response.xpath(business_start_date_xpath).get()
        item["complaints_l36m"] = response.xpath(complaints_l36m_xpath).get()
        item["complaints_l12m"] = response.xpath(complaints_l12m_xpath).get()

        yield item

    def parse(self, response: Response) -> Any:
        results_x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div/*'
        search_results = response.xpath(results_x_path)

        self.log(f"NUMBER OF ITEMS: {len(search_results)}")

        for item in search_results:
            contractor = self.get_contractor(item)
            if contractor["profile_page_url"]:
                request = scrapy.Request(
                    contractor["profile_page_url"],
                    callback=self.parse_contractor_profile,
                    cb_kwargs=dict(item=contractor),
                )
                yield request

        next_url_xpath = '//a[@rel="next"]/@href'
        next_url = response.xpath(next_url_xpath).get()
        if next_url and self.follow:
            yield response.follow(next_url, callback=self.parse)
