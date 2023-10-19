# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


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
