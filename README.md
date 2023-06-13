# scrapy

```bash
# access check
scrapy shell 'url'
# parse check
scrapy parse --spider=afpbb -c parse_item -d 2 'url'

# run
scrapy crawl afpbb --L INFO
```

## access check parse sample

```py
# url
>>> response.url
# number
>>> response.url.split('/')[-1]
# title
>>> response.css("h1::text").get()
# body
>>> response.css("div.article-body").get()
```

## refs

* <https://docs.scrapy.org/en/latest/intro/tutorial.html>
* <https://stackoverflow.com/questions/73389010/drop-requests-that-include-query-string-in-scrapy>
* <https://rinoguchi.net/2020/08/scrapy-manual.html>
* <https://ai-inter1.com/python-scrapy-for-begginer/>
* <https://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python>
