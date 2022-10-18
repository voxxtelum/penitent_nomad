import scrapy

class MCSPider(scrapy.Spider):
  name = 'cs_spider'
  allowed_domains = ['containerstore.com']
  handle_httpstatus_list = [301, 302, 307]
  
  cookies_list = {
    '_pxvid': "cce57c46-4a40-11ed-83b0-57684a6d7366",
    'AMCV_9E6BEED55732E6357F000101%40AdobeOrg': "1585540135%7CMCIDTS%7C19280%7CMCMID%7C53881646409190335419196646208678538628%7CMCOPTOUT-1665780666s%7CNONE%7CvVersion%7C4.4.0",
    'AMCVS_9E6BEED55732E6357F000101%40AdobeOrg': "1",
    'at_check': "true",
    'mbox': "PC#50ba82555f404850acac1248e5d05794.34_0#1729018267|session#159fed72cf124d67b7132e06204e056c#1665775327",
    'pxcts': "8cefe8a4-4bf0-11ed-b10e-496576437675",
    'customerId': "4363215900",
    'JSESSIONID': "4EC70AEEBEDC729F8A97E3786B288593.dfwintas18prd-inst115",
    'tcs_experiments': "\"eyJtZWdhTmF2IjoiQiIsImR1bW15IjoiQSIsInBkcCI6IkEiLCJlbGZhTGFuZGluZ1BhZ2UiOiJCIn0=\"",
    '__olapicU': "1665772853196",
    '_cou': "US",
    '_cur': "USD",
    '_pxhd': "Yuba398sd6sa6/Uowa-DiLuprp0kDZcJ85HGebFIljBR19zJDBOoaSBxnjSuk-qx9vM76RgtSxMyDfDLyfeLQw==:3L3rVQixfB8qS4zhkVzDKsMyEsM9cDVVbCOdvzMo5BoQAPhDv1V6Yt3ccEh44c/MpET0/oJAX6JXdE3xT1JDf9e43KIY9X3DxGL4wzAS2vg=",
    'CSRF_TOKEN': "5SjL2Z4hkXlhGmU2B4XTnNDUXQtRM1gadGZA4mw9QGyiF3CpMVEZvBVUXMNDyA5c",
    'eventSerializationId': "9F8A97E3786B28859300",
    'URID': "fyL1c22XYqkKXP3TvfvOrcVCRfwrNeozfgateAmUklsBzRfOJGg0TSIXsFE5aN6L"
  }

  def start_requests(self):
        
        urls = [
            'https://www.containerstore.com/locations/index.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    store_urls = response.css('.store-name.bem-text-body').xpath('./a/@href').extract()
    print('URLS')
    print(store_urls)
    for s in store_urls:
      s_url = 'https://www.containerstore.com' + s
      yield scrapy.Request(s_url ,meta={'dont_redirect': True}, callback=self.parse_store)

  def parse_store(self, response):

    store_add1 = response.css('.store-information-block').xpath('./div[1]//text()').getall()

    store_info = {}
    store_info['store_add1'] = store_add1[0]
    store_info['store_add2'] = store_add1[1]
    store_info['store_add3'] = store_add1[2]
    store_info['store_add4'] = store_add1[3]
    yield store_info
