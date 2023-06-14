import scrapy
from pathlib import Path
from afpbb.items import AfpbbItem
from w3lib import html
from scrapy.exceptions import CloseSpider


class AfpbbSpider(scrapy.Spider):
    name = "afpbb"
    allowed_domains = ["www.afpbb.com"]
    start_urls = ["https://www.afpbb.com/articles/-/3468222"]

    # oldest accessible article number at 2023-06-14
    oldest_number = 3300000

    handle_httpstatus_list = [404]

    def parse(self, response):
        self.logger.info(f"url: {response.url}")
        number = int(response.url.split("/")[-1])

        title = response.css("h1::text").get()
        self.logger.info(f"number: {number}, title: {title}")

        if response.status == 200 and title is not "記事はありません":
            text = response.css("div.article-body").get()

            # save html only when the file does not exist
            filename = f"html/{number}-article-from-afpbb.html"
            if not Path(filename).exists():
                Path(filename).write_bytes(response.body)

                # save plain text as well
                rm_aside = html.remove_tags_with_content(text, which_ones=("aside",))
                plain_text = html.replace_escape_chars(
                    html.remove_tags(rm_aside)
                ).strip()
                yield AfpbbItem(text=plain_text, url=response.url)

        if number >= self.oldest_number:
            next_page = f"https://www.afpbb.com/articles/-/{number - 1}"
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'dont_redirect': True})
        else:
            # stop crawling when the oldest article is reached
            # see: https://docs.scrapy.org/en/latest/topics/exceptions.html?highlight=closeSpider
            raise CloseSpider("Reached the oldest article, stopping crawling.")
