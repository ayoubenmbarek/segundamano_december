import scrapy
from scrapy_splash import SplashRequest
from segundamano.items import SegundamanoItem
from selenium import webdriver
class MySpider(scrapy.Spider):
    name = "splashspider"
    handle_httpstatus_list = [301, 302]#, 500]#, 403]
    allowed_domains = ['segundamano.mx']
    start_urls = ["https://www.segundamano.mx/anuncios/ciudad-de-mexico/miguel-hidalgo/renta-inmuebles/casa-en-renta-en-real-de-las-lomas-386984"]

    #def start_requests(self):
        #for url in self.start_urls:
           # yield scrapy.Request(url, meta={
            #    'splash': {
             #       'endpoint': 'render.html',
              #      'args': {'wait': 0.5}
               # }
           #})
         #run docker docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})#, endpoint='render.html',args={'js_source': 'document.title="My Title";'},)

    def parse(self, response):
	driver = webdriver.Chrome()
	for url in self.start_urls:
	        driver.get(url)
                item = SegundamanoItem()
                click_phone = driver.find_element_by_css_selector('.ar-CoverPhone.ar-CoverPhone_Text')
	        click_phone.click()
	        item["AGENCE_TEL"] = driver.find_element_by_css_selector('.phoneCont.ar-PhoneNumber.deskButton.v-cloak--hidden').text
                #----------------------
                
                address = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[1]/div/span').text 
                address1 = address.split('n:')
                item['ADRESSE'] = address1[-1]
                #------------------------------------
                #phone = driver.find_element_by_xpath(".//div[contains(text(), Superficie')]/following-sibling::span/text()").extract()
                
                #driver.find_element_by_css_selector('.av-AdInformation-info').text #full address
                
                #-------------------
                try:
                        item['Site'] = ''
                        date = driver.find_element_by_xpath('//div[@class="av-AdInformation_Column"]').text #publication
                        date1 = date.split('do:')
                        item['Site'] = date1[-1]
                        #---------------------
                        type_imm = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[3]/div/div/span').text
                        item["PHOTO"] = type_imm
                        #----------------------------------------
                        item["SURFACE_TERRAIN"] = ''
                        surface = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[5]/div/div/span').text
                        item["SURFACE_TERRAIN"] = surface
                        #---------------------------
                        #item['PIECE'] = ''
                        habita = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[4]/div/div/span').text
                        item['PIECE'] = habita
                        if item['SURFACE_TERRAIN'] == '':
                                item["SURFACE_TERRAIN"] = habita 
                except:
                        pass
                
                
                
                #----------------------------------------
                #//*[contains(@class, 'Test')]
                
                #phone = response.css('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[4]/div/div/span').extract()
                #following-sibling::span/text()').extract_first(default='')#.strip(' \n\t\r')
                
                
                #phone = response.xpath("//div[contains(text(), 'Tipo')]/preceding-sibling::div/text()").extract()
                #phone = response.xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[3]/div/div/span/text').extract()
                #phone = response.css('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[4]/div/div/span').extract()
                #phone = response.xpath('//div[@class="av-AdInformation-info"]/following-sibling::span/text()').extract_first()
                #phone = response.css('div.av-PhoneNumber ::text').extract()
                #phone = response.xpath('//*[@id="sw-Ad-reply-shop"]/div[3]/label[2]/text').extract()
                #cc = response.url #is a result of render.html call; it
                #kk = response.css('h2.sw-IsHidden ::text').extract()
                yield item
                # contains HTML processed by a browser.
                # ...
#to view phone number
#def start_requests(self):
  #      for url in self.start_urls:
      #      yield scrapy.Request(url, meta={
         #       'splash': {
            #        'endpoint': 'render.html',
                   # 'args': {'wait': 0.5}
              #  }
           # })

   # def parse(self, response):
     #   for question in response.css("div.bix-div-container"):
         #   answer = question.xpath(".//input[starts-with(@id, 'hdnAnswer')]/@value").extract()
          #  print answer
