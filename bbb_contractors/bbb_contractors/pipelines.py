# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime


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
            date = datetime.strptime(date, "%m/%d/%Y")
            return date.isoformat()

        date_fields = ["accredited_date", "business_start_date"]
        for field in date_fields:
            item[field] = clean_date(item[field])

        # impute complaints

        # parse reviews
