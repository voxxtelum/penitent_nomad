import scrapy
import re

class MCSPider(scrapy.Spider):
  name = 'ik_spider'
  allowed_domains = ['ikea.com']
  
  def start_requests(self):
        urls = [
            'https://www.ikea.com/us/en/stores/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    store_urls = response.css('.i1ycpxq9.pub__designSystemText.t91kxqv.w1fdzi2f').xpath('./p/a/@href').extract()
    print(store_urls)
    for s in store_urls:
      yield scrapy.Request(s, self.parse_store)


  def parse_store(self, response):

    def split_loc(location):
      # San Diego, CA 92108
      loc_split = location.split(',', 1)
      # print(loc_split)
      city = loc_split[0].strip()

      state_zip = re.sub('\s+', ' ', loc_split[1]).strip();
      state = state_zip.split(' ')[0].strip()
      zip = str(state_zip.split(' ')[1].strip())

      return [city, state, zip]

    store_data = response.css('.hnf-store__container__block').xpath('./p/text()').extract()

    loc_data = split_loc(store_data[2])

    # print(loc_data)
    # print("loc_data: " + loc_data[0])
    # print("loc_data: " + loc_data[1])

    store_name = re.sub('\s+', ' ', store_data[0]).strip().split('IKEA ')[1]
    store_add1 = re.sub('\s+', ' ', store_data[1]).strip()

    store_city = loc_data[0]
    store_state = loc_data[1]
    store_zip = loc_data[2]

    # print('store_name: ' + store_name)
    # print('store_add1 ' + store_add1)
    # print('store_city: ' + store_city)
    # print('store_state: ' + store_state)
    # print('store_zip: ' + store_zip)

    store_info = {}
    store_info['store_name'] = store_name
    store_info['store_add1'] = store_add1
    store_info['store_add2'] = ''
    store_info['store_city'] = store_city
    store_info['store_state'] = store_state
    store_info['store_zip'] = store_zip
    yield store_info

      

