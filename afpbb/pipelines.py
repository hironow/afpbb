# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
from datetime import datetime


class AfpbbPipeline:
    def __init__(self) -> None:
        # filename based on datetime as 'items-2021-01-01-00-00-00.jsonl'
        filename = f"items-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jsonl"
        self.file = open(filename, "wb")
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
