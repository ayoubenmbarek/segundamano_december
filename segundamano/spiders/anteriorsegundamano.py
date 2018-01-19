import scrapy
from scrapy import Request
from selenium import webdriver
from segundamano.items import SegundamanoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import ast
import json
import time
import re
from selenium.webdriver.common.by import By
from scrapy_splash import SplashRequest
from selenium import webdriver
from datetime import datetime  
from datetime import timedelta 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class segundamanoSpider(scrapy.Spider):
        name = "segundamanoanterior12-12"
        #name = "myspider"
        handle_httpstatus_list = [200, 301, 302]#, 500]#, 403]
	allowed_domains = ['segundamano.mx']
	#start_urls = ['http://www.inmuebles24.com/inmuebles-en-venta.html']
	start_urls = ['http://viejo.segundamano.mx/mexico/inmuebles?ca=11_s&cg=1000&et=0&o=1',
	               ]
	download_delay = 0
	
	def parse(self, response):
	        
	        
		for block in response.css('div.listing_thumbs_row'):
			myItem = SegundamanoItem()
                        img_number = block.css('div.thumbnail_photo_count ::text').extract_first()
                            
                        try: #added 12-12
                            num = img_number.split(' ')
                            num1 = num[0]
                            myItem["PHOTO"] = num1
                        except:   
                            pass
			#myItem["Site"] = response.url
		        url = block.css('a.listing_container ::attr(href)').extract_first()
		        request = scrapy.Request(url, callback=self.second_page)
		        request.meta['myItem'] = myItem
		        yield request

                next_page = response.xpath('//*[@class="resultcontainer"]/span/a/@href').extract()[-1]
		if next_page:
		        req = scrapy.Request(next_page,  callback=self.parse) 
		        yield req     
		 
                
        def second_page(self, response):
                hxs = Selector(response)
                myItem = response.meta["myItem"] 
                #items = response.xpath('//script/text()').re(".*@context.*") 
		list_uniq_linq = []
		link = response.url
		myItem["ANNONCE_LINK"] = link#.split()
		try:
		    myItem['PIECE'] = response.xpath('//ul/li[contains(text(), "Habitaciones")]/strong/text()').extract_first()
                except:
                    pass
                try:
		    myItem["M2_TOTALE"] = response.xpath('//ul/li[contains(text(), "Superficie")]/strong/text()').extract_first()
                except:
                    pass
                try:
		    myItem["CATEGORIE"] = response.xpath('//ul/li[contains(text(), "Tipo de inmueble")]/strong/text()').extract()
                except:
                    pass
		    
		specific_words_terrain = ['terreno', 'Terreno', 'TERRENO',]
	        specific_words_casa = ['casa', 'Casa', 'CASA']
	        specific_words_departmnent = ['departamento', 'Departamento', 'DEPARTAMENTO']
                specific_words_residencial = ['Resid','residencial', 'Residencial', 'RESIDEN']
                    #if myItem["CATEGORIE"] is None:
                if not myItem["CATEGORIE"]:# == []:
		            
		        for word in specific_words_terrain:
		            if word in myItem["ANNONCE_LINK"]:
		                myItem["CATEGORIE"] == ['Terrenos']
                        for word in specific_words_residencial:
                              if word in myItem["ANNONCE_LINK"]:
                                   myItem["CATEGORIE"] == ['Immeuble']
	                
		        for word in specific_words_casa:
		            if word in myItem["ANNONCE_LINK"]:
		                 myItem["CATEGORIE"] == ['Casas']
		                    
                        for word in specific_words_departmnent:
		            if word in myItem["ANNONCE_LINK"]:
		                 myItem["CATEGORIE"] == ['Departamentos']
		                
                if myItem["CATEGORIE"] == ['Departamentos']:
                        myItem["MAISON_APT"] = 2
                if myItem["CATEGORIE"] == ['Immeuble']:                                                                                                       
                        myItem["MAISON_APT"] = 7
                elif myItem["CATEGORIE"] == ['Casas']:
                         myItem["MAISON_APT"] = 1
                elif  myItem["CATEGORIE"] == ['Terrenos']: 
                           myItem["MAISON_APT"] = 6
                elif  myItem["CATEGORIE"] == ['Oficinas/locales']: 
                           myItem["MAISON_APT"] = 5
                elif  myItem["CATEGORIE"] == ['Bodegas']:                                                                                             
                           myItem["MAISON_APT"] = 4
                elif  myItem["CATEGORIE"] == ['Otros']:
                            myItem["MAISON_APT"] = 8
                else:
                    myItem["MAISON_APT"] = 0


                myItem["SITE"] =  'segundamano'       
                try:
                    #myItem["ANNONCE_TEXT"] = response.xpath('//p[@class="av-AdDescription"]').extract()
    		    myItem["ANNONCE_TEXT"] = response.xpath('.//meta[@name="description"]/@content').extract_first()
                except:
                    pass
                try:
		    myItem["AGENCE_NOM"] = response.xpath('.//*[@class="primarycolor bold"]/text()').extract_first()
                except:
                    pass
                try:
		    myItem["FROM_SITE"] = 'segundamano'
                except:
                    pass
                try:
		    cc = response.css('title ::text').extract_first()
                    bb = cc.split(',')
                    myItem["NOM"] = bb[0]

                   # myItem["NOM"] = response.xpath('//h1[@class="av-AdTitle"]/text()').extract_first()
                except:
                    pass
                try:
		    #myItem["REGION"] = response.xpath('.//*[@class="right_col"]/li/strong/text()').extract_first()
		    vv = response.xpath('//ul/li[contains(text(), "Colonia")]/strong/text()').extract_first() 
                    if vv == 'Otra':
                        myItem["QUARTIER"] = ''
                    else:
                        myItem["QUARTIER"] = vv
                except:
                    pass
                try:
		    myItem["VILLE"] = response.xpath('.//*[@class="parameter"]/text()').extract_first()
                except:
                    pass
		    #myItem["PHOTO"] = response.xpath('.//*[@id="display_image"]/img/@src').extract_first() #commented 12-12
		if 'renta' in  myItem["ANNONCE_LINK"]:
		        myItem["ACHAT_LOC"] = 2
	        elif 'venta' in myItem["ANNONCE_LINK"]:
	                myItem["ACHAT_LOC"] = 1
                elif 'traspasos' in myItem["ANNONCE_LINK"]:
                    myItem["ACHAT_LOC"] = 'traspasos'
	        else:
                    myItem["ACHAT_LOC"] = ''    
                try:
                    myItem["PROVINCE"] = response.css('h3.nav_element ::text').extract_first() 
                except:
                    pass
                #except:
                 #   pass
                try:
                    myItem["AGENCE_ADRESSE"] = 	myItem["VILLE"]+','+ myItem["PROVINCE"]
                except:
                    pass
                try:
                    myItem["AGENCE_VILLE"] = response.css('h3.nav_element ::text').extract_first()
                except:
                    pass
                try:
                    myItem["ADRESSE"] = myItem["QUARTIER"]+','+ myItem["VILLE"]+','+ myItem["PROVINCE"]
                except:
                    pass
                
		items = response.xpath('//script/text()').re(".*account_id.*")
	        items1 = items[0]
                items2 = items1.split('attrs:')
                items3 = items2[-1]                        
                items4 = items3.split('},')
                items5 = '}'.join(items4)
                json_co = json.loads(items5)
                try:
                    myItem["PRIX"] = json_co.get('price')#+'$'
                except:
                    pass
                try:
                    myItem["AGENCE_TEL"] = json_co.get('phone')
                except:
                    pass
                try:
                    myItem['ANNONCE_DATE'] = json_co.get('orig_date')
                except:
                    pass
                try:
                    myItem["EMAIL"] = json_co.get('email') 
                except:
                    pass
                myItem["ID_CLIENT"] = re.search(r'_(.*?).htm', myItem["ANNONCE_LINK"] ).group(1)
                #try:
                #    myItem["ID_CLIENT"] = json_co.get('account_id') 
                #except:
                #    pass
                try:
                    myItem["PAYS_DEALER"] = 'Mexique'
                except:
                    pass
                vv = response.css('div.AdHeaderBar > span ::text').extract_first()
                if 'profesional' in vv:
                    myItem["SELLERTYPE"] = 'professionel'
                else:
                    myItem["SELLERTYPE"] = 'particulier'
                        
		    
#		except:
#		        pass    
		yield myItem        

		
	        
                    
         

		
	         
	         
	                        
	        #myItem["AGENCE_VILLE"] = json_items.get('offers', {}).get('seller', {}).get('address', {}).get('addressLocality')
                
                #myItem["MINI_SITE_ID"] = page_id2[-2]

                #myItem["NEUF_IND"] =
                #myItem["CP"] =
                #myItem["REGION"] = new_dict2.get('barrio')
                #myItem["ETAGE"] =
                #myItem["NB_ETAGE"] =
                #myItem["LATITUDE"] = response.xpath('//*[@id="lat"]/@value').extract()
                #myItem["LONGITUDE"] = response.xpath('//*[@id="lng"]/@value').extract()
                #myItem["M2_TOTALE"] = all_s[7]
                #myItem["NB_GARAGE"] =
                
                #myItem["PRIX_M2"] =
                #myItem["URL_PROMO"] =
                #myItem["PAYS_AD"] =
                #myItem["PRO_IND"] =
                #myItem["MINI_SITE_ID"] =
                #myItem["FLUX"] =
                #myItem["SITE_SOCIETE_URL"] =
                #myItem["SITE_SOCIETE_ID"] =
                #myItem["SITE_SOCIETE_NAME"] =
                #myItem["AGENCE_RCS"] =
                #myItem["SPIR_ID"] =
                #myItem["AGENCE_VILLE"] =
                #myItem["WEBSITE"] =
                #myItem["AGENCE_TEL_2"] =
                #myItem["AGENCE_TEL_3"] =
                #myItem["AGENCE_TEL_4"] =
                #myItem["AGENCE_FAX"] =
                #myItem["AGENCE_CONTACT"] =
                
                
                yield myItem







