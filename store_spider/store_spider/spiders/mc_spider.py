import scrapy

class MCSPider(scrapy.Spider):
  name = 'mc_spider'
  allowed_domains = ['microcenter.com']
  
  def start_requests(self):
        urls = [
            'https://www.microcenter.com/site/stores/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    store_urls = response.xpath('//div[@class="location-container"]/div/a/@href').extract()
    for s in store_urls:
      s_url = 'https://www.microcenter.com' + s
      yield scrapy.Request(s_url, self.parse_store)

  def parse_store(self, response):
    store_name = response.xpath('//*[@id="content"]/div[4]/div/div[1]/h2/text()').get()
    store_add1 = response.xpath('//div[@id="StoreAddress"]/div[@class="address"]/div[1]/text()').get()
    store_add2 = response.xpath('//div[@id="StoreAddress"]/div[@class="address"]/div[2]/text()').get()
    store_city = response.xpath('//div[@id="StoreAddress"]/div/div[3]/span[1]/text()').get()
    store_state = response.xpath('//div[@id="StoreAddress"]/div/div[3]/span[2]/text()').get()
    store_zip = response.xpath('//div[@id="StoreAddress"]/div/div[3]/span[3]/text()').get()

    store_info = {}
    store_info['store_name'] = store_name
    store_info['store_add1'] = store_add1
    store_info['store_add2'] = store_add2
    store_info['store_city'] = store_city
    store_info['store_state'] = store_state
    store_info['store_zip'] = str(store_zip)
    yield store_info

      

