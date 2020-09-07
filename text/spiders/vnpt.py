import scrapy
import html2text
from scrapy.loader import ItemLoader
from text.items import TextItem

class VnptSpider(scrapy.Spider):
    name = 'vnpt'
    start_urls = ['https://vnpt.com.vn/']

    def parse(self, response):
        urls = []
        l = ItemLoader(item=TextItem())

        path = response.xpath('//ul[@class="clearfix menuPc"]//a')
        for url in path:
            urls.append(url.attrib['href'])
        urls = urls[0:urls.index('/ho-tro')]

        for url in urls:
            if not (('https' in url) or ('http' in url)):
                urls[urls.index(url)] = 'https://vnpt.com.vn' + url

        for url in urls:
            l.add_value('url', url)
            yield scrapy.Request(url=url, callback=self.parse_page,meta={'loader':l})
        # l.add_value('url','https://vnpt.com.vn/goi-home/home-combo')
        # yield scrapy.Request(url='https://vnpt.com.vn/goi-home/home-combo', callback=self.parse_page,meta={'loader':l})

    def parse_page(self, response):
        l = ItemLoader(item=TextItem(),parent=response.meta['loader'])

        html = response.xpath('//div[@class="container"]').extract()
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        for text in html:
            l.add_value('text',h.handle(text))

        yield l.load_item()
        # print(h.handle(html))
