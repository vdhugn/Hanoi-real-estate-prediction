import scrapy

class HREPSpider(scrapy.Spider):
    name = 'hrep'
    allowed_domains = ['nhadat24h.net']
    start_urls = [f'https://nhadat24h.net/nha-dat-ban-ha-noi/page{i}' for i in range(1, 2236)]

    def parse(self, response):
        for item in response.xpath('//div[@class="dv-item"]'):
            if item.xpath('.//div[@class="review1"]/a[1]/text()').get() in ['Nhà trong ngõ', 'Nhà mặt phố']:
                location = item.xpath('.//label[@class="rvVitri"]/span/text()').get()
                details = item.xpath('.//div[@class="reviewproperty1"]/label[not(@class="rvVitri") and not(@class="lb-des")]/span/text()').getall()
                yield {
                    'price': item.xpath('.//label[@class="a-txt-cl1"]/text()').get(),
                    'area': item.xpath('.//label[@class="a-txt-cl2"]/text()').get(),
                    'type': item.xpath('.//div[@class="review1"]/a[1]/text()').get(),
                    'district': next((elem for elem in location.split(', ') if 'Quận' in elem), None),
                    'road_width': next((elem for elem in details if 'Rộng' in elem), None),
                    'width': next((elem for elem in details if 'Mặt tiền' in elem), None),
                    'floors': next((elem for elem in details if 'tầng' in elem), None),
                    'parking_slots': next((elem for elem in details if 'ôtô' in elem), None),
                    'bedrooms': next((elem for elem in details if 'ngủ' in elem), None),
                    'bathrooms': next((elem for elem in details if 'WC' in elem), None),
                }
        