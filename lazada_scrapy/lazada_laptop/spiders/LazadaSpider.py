import scrapy
from ..items import LazadaLaptopItem
from selenium import webdriver
from scrapy.utils.project import get_project_settings


class LazadaspiderSpider(scrapy.Spider):
    name = 'LazadaSpider'
    def start_requests(self):
        url = ['https://www.lazada.vn/giay-sneaker-nam/?q=gi%C3%A0y+sneaker&from=input',
               'https://www.lazada.vn/giay-sneaker-nam/?from=input&page=2&q=gi%C3%A0y%20sneaker',
               'https://www.lazada.vn/giay-sneaker-nam/?from=input&page=3&q=gi%C3%A0y%20sneaker',]
        for item in url:
            settings= get_project_settings()
            driver_path = settings['CHROME_DRIVER_PATH']
            options= webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(driver_path, options=options)
            driver.get(item)
            link_elements = driver.find_elements_by_xpath(
                 '//*[@data-qa-locator="product-item"]//a[text()]'
            )
            for link in link_elements:
                yield scrapy.Request(link.get_attribute('href'), callback=self.parse)
            driver.quit()


    def parse(self, response):
        #<h1 class="pdp-mod-product-badge-title">Xtep Giày nam Giày sneaker Giày đôi màu đen trắng phong cách Hàn Quốc cho nam sinh đại học thanh thiếu niên Giày đế dày sành điệu dễ phối 881219319851</h1>
        name= response.xpath('//h1[@class="pdp-mod-product-badge-title"]//text()').get()
        #<img class="pdp-mod-common-image gallery-preview-panel__image" src="//my-live-05.slatic.net/p/f925aa0ad6f7e6c1e1508ada94ab0938.jpg_720x720q80.jpg_.webp" alt="Xtep Giày nam Giày sneaker Giày đôi màu đen trắng phong cách Hàn Quốc cho nam sinh đại học thanh thiếu niên Giày đế dày sành điệu dễ phối 881219319851">
        image = response.css('.gallery-preview-panel__image').css("::attr(src)").extract()
        #<img class="pdp-mod-common-image gallery-preview-panel__image" src="//my-live-05.slatic.net/p/f925aa0ad6f7e6c1e1508ada94ab0938.jpg_720x720q80.jpg_.webp" alt="Xtep Giày nam Giày sneaker Giày đôi màu đen trắng phong cách Hàn Quốc cho nam sinh đại học thanh thiếu niên Giày đế dày sành điệu dễ phối 881219319851">
        brand = response.xpath('//a[@class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link"]/text()').getall()
        #<<a class="pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name" target="_self" href="//www.lazada.vn/shop/xtep-official-store/?itemId=348608175&amp;channelSource=pdp">XTEP Official Store</a>
        name_seller = response.xpath('//a[@class="pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name"]/text()').get()
        #<span class=" pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl">531.000 ₫</span>
        price = response.xpath('//span[@class="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]//text()').getall()
        #<div class="seller-info-value rating-positive ">97%</div>
        positive_rating =  response.xpath('//div[@class="seller-info-value rating-positive "]/text()').get()
        #<div style="color:" class="seller-info-value ">96%</div> #//*[@id="module_seller_info"]/div/div[2]/div[2]/div[2]
        delivered_on_time = response.xpath('//div[@class="info-content"][2]/div[2]/text()').get()
        #delivered_on_time = response.xpath('//div[@class="info-content"][2]/div[2]/text()').get() #//*[@id="module_seller_info"]/div/div[2]/div[3]/div[2]
        response_rate = response.xpath('//div[@class="info-content"][3]/div[2]/text()').get()
        #<div class="delivery-option-item__time" data-spm-anchor-id="a2o4n.pdp_revamp.delivery_options.i0.3dca23afmvGmU4">8 - 16 ngày</div>
        delivery_time = response.xpath('//div[@class="delivery-option-item__time"]/text()').get()
        #<div class="delivery-option-item__shipping-fee no-subtitle">12.900 ₫</div>
        transport_fee = response.xpath( '//div[@class="delivery-option-item__shipping-fee no-subtitle"]/text()').get()
        
       
        item= LazadaLaptopItem()
        item['name']=name
        item['image']=image
        item['brand']=brand
        item['name_seller']=name_seller
        item['price']=price
        item['positive_rating']=positive_rating
        item['delivered_on_time']=delivered_on_time
        item['response_rate']=response_rate
        item['delivery_time']=delivery_time
        item['transport_fee']=transport_fee
        
        yield item

        