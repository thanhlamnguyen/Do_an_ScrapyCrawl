# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaLaptopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    brand = scrapy.Field()
    name_seller = scrapy.Field()
    price = scrapy.Field()
    positive_rating = scrapy.Field()
    delivered_on_time = scrapy.Field()
    response_rate = scrapy.Field()
    delivery_time = scrapy.Field()
    transport_fee = scrapy.Field()
    