import scrapy
#import requests
import logging
import json
#from urlparse import urlparse
from scrapy import signals
from scrapy import Spider
import re
from scrapy.utils.trackref import NoneType


class VDPVehicleInfo(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    stock_no = scrapy.Field()
    vin = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()


class VehicleInfo(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    ext_color = scrapy.Field()
    int_color = scrapy.Field()
    stock_no = scrapy.Field()
    miles = scrapy.Field()
    vin = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    veh_state = scrapy.Field()
    image = scrapy.Field()
    engine = scrapy.Field()
    transmission = scrapy.Field()
    drivetrain = scrapy.Field()
    body_style = scrapy.Field()
    carfax = scrapy.Field()
    fuel_type = scrapy.Field()
    fuel_combined = scrapy.Field()
    fuel_highway = scrapy.Field()
    fuel_city = scrapy.Field()
    doors = scrapy.Field()
    induction = scrapy.Field()
    displacement = scrapy.Field()
    cylinder = scrapy.Field()
    price_type = scrapy.Field()
    body_type = scrapy.Field()
    description = scrapy.Field()


class {domain_under}(scrapy.Spider):
    name = '{domain_under}'
    domain = '{domain_under}'
    allowed_domains = ['{domain}']
    start_urls = ['https://www.{domain}/inventory?type=new', 'https://www.{domain}/inventory?type=used']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 10,
        #'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_FAIL_ON_DATALOSS': 'false',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'ACCEPT_ENCODING': 'gzip, deflate, br',
            'ACCEPT_LANGUAGE': 'en-US,en;q=0.9',
            'CONNECTION': 'keep-alive',
        }
    }
    '''i = 0

    def _url(self, path):
        return 'http://fbi.targetmediapartners.com' + path

    def get_current_ip(self):
        header_info = {'Content-Type': 'application/json'}
        r = requests.get('http://ipinfo.io', headers=header_info)
        logging.warning(r.status_code)
        logging.warning(r.text)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(manlyhonda_com, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self):
        self.update_progress('done')

    def update_progress(self, status):
        post_info = {"domain": self.domain, "count": self.i, "status": status, "notes": self.crawler.stats.get_stats()}
        logging.warning(json.dumps(post_info, default=str, sort_keys=True))
        header_info = {'Content-Type': 'application/json', 'Api-Key': 'api-key-1234567890'}
        resp = requests.post(self._url('/Status/Crawler'), data=json.dumps(post_info, default=str, sort_keys=True),
                             headers=header_info)'''

    def parse(self, response):
        resp = response.css('div.srp-vehicle-container > div.srp-vehicle')
        if resp:
            pass
        else:
            resp = response.xpath('//*[@class="row srp-vehicle"]')
        for listing in resp:
            urls = listing.css('h2.srp-vehicle-title > a::attr(href)').extract()
            if len(urls) > 0:
                urls = listing.css('h2.srp-vehicle-title > a::attr(href)').extract()
            else:
                urls = listing.css('h4 > a::attr(href)').extract()
            data = {
                "year": listing.css('meta[itemprop="releaseDate"]::attr(content)').extract_first(),
                "title": listing.css('meta[itemprop="name"]::attr(content)').extract_first(),
                "make": listing.css('meta[itemprop="brand"]::attr(content)').extract_first(),
                "model": listing.css('meta[itemprop="model"]::attr(content)').extract_first(),
                "ext_color": listing.css('meta[itemprop="color"]::attr(content)').extract_first(),
                "stock_no": listing.css('meta[itemprop="sku"]::attr(content)').extract_first(),
                "veh_state": listing.css(".srp-vehicle-title a::text").extract_first()
            }
            for url in urls:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_details, meta=data)
        if (self.domain == "freemantoyota.com") or (self.domain == "dchmontclairacura.com"):
            responsedUrls = response.xpath('//li[@class="arrow"]/a/@href').extract()[-1]
            if not isinstance(responsedUrls, NoneType):
                responsedUrls = response.urljoin("/"+''.join(responsedUrls.split("/inventory")))
                yield response.follow(url=responsedUrls, callback=self.parse)
        else:
            responsedUrls = response.css('ul.pagination:last-child > li.arrow:last-child > a:last-child')
            for next_page in responsedUrls:
                yield response.follow(next_page, self.parse)

    def parse_details(self, response):
        listing = response
        vehicle = VehicleInfo()
        vehicle['domain'] = self.domain

        if response.meta["year"]:
            vehicle['year'] = response.meta["year"]
        elif response.meta["title"]:
            vehicle['year'] = response.meta["title"].split(" ")[0]

        if vehicle['year']:
            vehicle['url'] = response.request.url
            vehicle['title'] = response.meta["title"]
            vehicle['make'] = response.meta["make"]
            vehicle['model'] = response.meta["model"]
            vehicle['ext_color'] = response.meta["ext_color"]
            vehicle['stock_no'] = response.meta["stock_no"]
            vehicle['veh_state'] = response.meta["veh_state"]

            if vehicle['veh_state']:
                vehicle['veh_state'] = vehicle['veh_state'].strip()

            vin = listing.xpath('.//li/span[contains(text(), "VIN")]/../text()').extract_first()
            if vin != " ":
                if vin:
                    vehicle['vin'] = vin.strip()
            else:
                vehicle['vin'] = listing.xpath('.//li/span[contains(text(), "VIN")]/../text()').extract()[not None].strip()

            vehicle['int_color'] = listing.xpath(
                './/li/span[contains(text(), "Int. Color:")]/../text()').extract_first()
            if vehicle['int_color']:
                vehicle['int_color'] = vehicle['int_color'].strip()

            vehicle['engine'] = listing.xpath('.//li/span[contains(text(), "Engine:")]/../text()').extract_first()
            if vehicle['engine']:
                vehicle['engine'] = vehicle['engine'].strip()

            vehicle['transmission'] = listing.xpath(
                './/li/span[contains(text(), "Transmission:")]/../text()').extract_first()
            if vehicle['transmission']:
                vehicle['transmission'] = vehicle['transmission'].strip()

            vehicle['drivetrain'] = listing.xpath(
                './/li/span[contains(text(), "Drive Type:")]/../text()').extract_first()
            if vehicle['drivetrain']:
                vehicle['drivetrain'] = vehicle['drivetrain'].strip()

            vehicle["body_style"] = listing.xpath(
                './/li/span[contains(text(), "Body Style:")]/../text()').extract_first()
            if vehicle['body_style']:
                vehicle['body_style'] = vehicle['body_style'].strip()

            vehicle['miles'] = listing.xpath('.//li/span[contains(text(), "Mileage:")]/../text()').extract_first()
            if vehicle['miles']:
                vehicle['miles'] = vehicle['miles'].strip()
            else:
                vehicle['miles'] = 0

            fuel_highway = listing.css("div.vdp-vehicle-mpg-hwy::text").extract_first()

            # check null value
            if not isinstance(fuel_highway, NoneType):
                vehicle['fuel_highway'] = fuel_highway.strip()
            else:
                vehicle['fuel_highway'] = "0"

            fuel_city= listing.css("div.vdp-vehicle-mpg-city::text").extract_first()

            # check null value
            if not isinstance(fuel_city, NoneType):
                vehicle['fuel_city'] = fuel_city.strip()
            else:
                vehicle['fuel_city'] = "0"

            price = listing.css('span[itemprop="price"]::text').extract_first()

            #check null value
            if not isinstance(price, NoneType):
                if price:
                    vehicle['price'] = price.replace("$", "").replace(",", "")
            else:
                vehicle['price'] = listing.css('span[itemprop="price"]::attr("content")').extract_first()

            vehicle['image'] = ""
            for img in response.css('a[data-zoom-id="vehicleGallery"]::attr(href)'):
                vehicle['image'] += img.extract() + ","

            vehicle['description'] = ''.join(listing.xpath('//*[@id="panel1"]/div[1]/text()').extract()).replace('\n', '').replace('\t', '')[:97] + "..."

            #self.i += 1
            #self.update_progress("in-progress")
            yield vehicle