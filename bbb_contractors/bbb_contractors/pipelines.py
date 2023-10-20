# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import re


class FilterWaterproofPipeline:
    def process_item(self, item, spider):
        filter_terms = ["waterproof", "waterproofing"]
        filter_field = "company_types"

        adapter = ItemAdapter(item)
        field = adapter.get(filter_field)
        if field:
            if any([term in field.lower() for term in filter_terms]):
                raise DropItem(
                    f"Company type is not valid, contains '{', '.join(filter_terms)}'"
                )
            else:
                item[filter_field] = field.replace(",", "|")

        return item


class CleanDataInputsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # clean dates
        def clean_date(date: str) -> str:
            date = datetime.strptime(date.strip(), "%m/%d/%Y")
            return date.isoformat()

        date_fields = ["accredited_date", "business_start_date"]
        for field in date_fields:
            value = adapter.get(field)
            if value:
                item[field] = clean_date(value)

        # parse reviews
        def get_digits(s: str) -> str:
            match = re.search(r"\d+", s)
            return match.group()

        review_count_field = "customer_review_count"
        review_count = adapter.get(review_count_field)

        if review_count:
            item[review_count_field] = get_digits(review_count)

        # parse rating
        rating_field = "customer_rating_avg"
        rating = adapter.get(rating_field)
        if rating:
            item[rating_field] = float(rating.replace("/5", ""))

        # impute complaints
        complaint_fields = ["complaints_l12m", "complaints_l36m"]
        for field in complaint_fields:
            value = adapter.get(field)
            if not value:
                item[field] = 0

        return item
