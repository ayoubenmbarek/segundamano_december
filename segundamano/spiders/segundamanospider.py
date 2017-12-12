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
from selenium.webdriver.common.by import By
from scrapy_splash import SplashRequest
from selenium import webdriver
from datetime import datetime  
from datetime import timedelta 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class segundamanoSpider(scrapy.Spider):
        name = "segundamanospider"
        handle_httpstatus_list = [301, 302]#, 500]#, 403]
	allowed_domains = ['segundamano.mx']
	#start_urls = ['http://www.inmuebles24.com/inmuebles-en-venta.html']
	start_urls = ['https://www.segundamano.mx/anuncios/mexico/inmuebles',
	               ]
	download_delay = 0
	
	def parse(self, response):
	
                myItem = SegundamanoItem()
                myItem["Site"] = response.url  #get all data from json on script tag        
                container = response.css('div.ad-card-wrapper')
                items = response.xpath('//script/text()').re(".*@context.*")
                unicode_items = items[0]
                json_items = json.loads(unicode_items)
                for jsonresponse in json_items.get('itemListElement', []):
                        item_url = jsonresponse.get('item', {}).get('url')
                        #item_url = jsonresponse.get('url')
                        request = SplashRequest(item_url, args={'wait': 0.5}, callback = self.second_page)#, dont_filter=True) 
                        request.meta['myItem'] = myItem
                        yield request


                #for link in container:
                      
                      #url = link.css('a.wrapped-link ::attr(href)').extract_first()
                      #full_url = response.urljoin(url)
                      #request = Request(full_url, callback = self.second_page)#, dont_filter=True) 
                      #request.meta['myItem'] = myItem
                      #yield request
                      
		for i in range(1,5944):
                        next_page = 'https://www.segundamano.mx/anuncios/mexico/inmuebles?page=' + str(i)    
                        yield scrapy.Request(next_page)    
                #linkcontainer = response.css('li.pagination-action-next')
                #for cc in linkcontainer:
                        #next_page = cc.css('a ::attr(href)').extract_first()
                        #if next_page:
                            #yield scrapy.Request(
                            #response.urljoin(next_page))

	        #next_page = response.css('a.more-products-btn.has-infinite ::attr(href)').extract_first()
                #if next_page:
                    #yield scrapy.Request(
                        #response.urljoin(next_page))#,callback=self.parse)                      
                
        def second_page(self, response):
                hxs = Selector(response)
                myItem = response.meta["myItem"] 
                items = response.xpath('//script/text()').re(".*@context.*") 
		list_department = ['Minidepartamento', 'departamento', 'departamentos']
		list_terrain = ['Terrenos','Terreno']
		list_casas = ['casa', 'casas']
		myItem["ANNONCE_LINK"] = response.url
		driver = webdriver.Chrome()
		driver.get(myItem["ANNONCE_LINK"])
	        #ar-CoverPhone ar-CoverPhone_Text
		#try:
                    #click_phone = WebDriverWait(driver, 10).until(
                      #  EC.presence_of_element_located((By.className, 'ar-CoverPhone'))#.ar-CoverPhone_Text
                    #)
                    #click_phone.click()
		   # myItem["AGENCE_TEL"] = driver.find_element_by_css_selector('.phoneCont.ar-PhoneNumber.deskButton.v-cloak--hidden::before').text
                    
                #finally:
                    #driver.quit()
                #try:    
	        #click_phone = driver.find_element_by_css_selector('.ar-CoverPhone.ar-CoverPhone_Text')
	        #click_phone.click()
	        #myItem["AGENCE_TEL"] = driver.find_element_by_css_selector('.phoneCont.ar-PhoneNumber.deskButton.v-cloak--hidden').text
	        
	        #address = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[1]/div/span').text 
                #address1 = address.split('n:')
                #myItem['ADRESSE'] = address1[-1]
                
                try:    
                        click_phone = driver.find_element_by_css_selector('.ar-CoverPhone.ar-CoverPhone_Text')
	                click_phone.click()
	                myItem["AGENCE_TEL"] = driver.find_element_by_css_selector('.phoneCont.ar-PhoneNumber.deskButton.v-cloak--hidden').text
	                
	                address = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[1]/div/span').text 
                        address1 = address.split('n:')
                        myItem['ADRESSE'] = address1[-1]
                        myItem['ANNONCE_DATE'] = ''
                        date = driver.find_element_by_xpath('//div[@class="av-AdInformation_Column"]').text #publication
                        date1 = date.split('do:')
                        myItem['ANNONCE_DATE'] = date1[-1]
                        #---------------------
                        #type_imm = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[3]/div/div/span').text
                        #item["CATEGORIE"] = type_imm
                        #----------------------------------------
                        myItem["SURFACE_TERRAIN"] = ''
                        surface = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[5]/div/div/span').text
                        myItem["SURFACE_TERRAIN"] = surface
                        #---------------------------
                        #item['PIECE'] = ''
                        habita = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[4]/div/div/span').text
                        myItem['PIECE'] = habita
                        if myItem['SURFACE_TERRAIN'] == '':
                                myItem["SURFACE_TERRAIN"] = habita 
                except:
                        pass
                
	        time.sleep(1)
                driver.quit()
		#finally:
	        #driver.quit()

		
		try:
                        unicode_items = items[0]
		        json_items = json.loads(unicode_items)
		        myItem["ANNONCE_TEXT"] = json_items.get('description')
		        myItem["NOM"] = json_items.get('name')
		         
		         
		                        
		        #myItem["CATEGORIE"] = json_items.get('category')
		        achat_loc = json_items.get('category')
			if 'Renta' in achat_loc:
				myItem["ACHAT_LOC"] = 2
			else:
				myItem["ACHAT_LOC"] = 1
				
		        myItem["PHOTO"] = json_items.get('image')
		        prix = json_items.get('offers', {}).get('price')
		        currency = json_items.get('offers', {}).get('priceCurrency')
			#myItem["ANNONCE_DATE"] = json_items.get('offers', {}).get('availabilityStarts')# available also with webdriver
		        myItem["PRIX"] = prix + currency
		        myItem["DEPARTEMENT"] = json_items.get('offers', {}).get('areaServed', {}).get('address', {}).get('addressCountry', {}).get('name')
		        myItem["VILLE"] = json_items.get('offers', {}).get('areaServed', {}).get('address', {}).get('addressLocality')
		        myItem["REGION"] = json_items.get('offers', {}).get('areaServed', {}).get('address', {}).get('addressRegion')
		        myItem["SELLERTYPE"] = json_items.get('offers', {}).get('seller', {}).get('@type')
		        myItem["AGENCE_NOM"] = json_items.get('offers', {}).get('seller', {}).get('name')
		        myItem["AGENCE_VILLE"] = json_items.get('offers', {}).get('seller', {}).get('address', {}).get('addressLocality')
		        agence_region = json_items.get('offers', {}).get('seller', {}).get('address', {}).get('addressRegion')
		        myItem["AGENCE_ADRESSE"] = myItem["AGENCE_VILLE"] +','+ agence_region
		        myItem["AGENCE_DEPARTEMENT"] = json_items.get('offers', {}).get('seller', {}).get('address', {}).get('addressCountry', {}).get('name')
		        text = json_items.get('description')
		        nom = json_items.get('name')	
		        
		        #for x in zip(list_department, list_terrain, list_casas):
                        #if 'Departamento' in nom or 'departamento' in text :
                           #     myItem["CATEGORIE"] = 'Departamentos'
                        #elif 'terreno' in nom or 'terreno' in text :    
                        #       myItem["CATEGORIE"] = 'Terrenos'
                       # elif 'Casa' in nom or 'casa' in text:
                        ##       myItem["CATEGORIE"] = 'Casas'
                        #elif 'Oficina' in nom or 'oficina' in text: 
                       #        myItem["CATEGORIE"] = 'Oficinas/locales'
                        #elif 'Consultorio' in nom or 'consultorio' in text: 
                       ##         myItem["CATEGORIE"] = 'Oficinas/locales'
                       #else:
                       #         myItem["CATEGORIE"] = '' 
                        type_imm = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[4]/div[1]/div[5]/div[3]/div/div/span').text
                        myItem["CATEGORIE"] = type_imm   
                        if myItem["CATEGORIE"] == 'Departamentos':
                                myItem["MAISON_APT"] = 2
                        elif  myItem["CATEGORIE"] == 'Casas': 
                                myItem["MAISON_APT"] = 1
                        elif  myItem["CATEGORIE"] == 'Terrenos': 
                                myItem["MAISON_APT"] = 6
                        elif  myItem["CATEGORIE"] == 'Oficinas/locales': 
                                myItem["MAISON_APT"] = 5
                        else:
                                myItem["MAISON_APT"] = ''
		
                except:
			pass
		
                       	 
                #myItem["Site"] = 'www.segundamano.mx/anuncios/mexico/inmuebles'
                try:
                        d = myItem["ANNONCE_LINK"].split('-')
                        myItem["ID_CLIENT"] = d[-1]
                        myItem["FROM_SITE"] = 'segundamano'
                        
                        #publication = items = response.xpath('//script/text()').re(".*published.*")
                        #cc = publication[0] 
                        #cc1 = cc.split('hed:')
                        #myItem["ANNONCE_DATE"] = cc1[-1]
                        
                        page_id = response.xpath('//script/text()').re(".*pageId.*")
                        page_id1 = page_id[0]
                        page_id2 = page_id1.split('"')
                        myItem["MINI_SITE_ID"] = page_id2[-2]
                except:
                        pass

                #myItem["NEUF_IND"] =
                #myItem["ADRESSE"] = response.xpath('//*[@id="map"]/div[1]/div/ul/li/text()').extract()
                #myItem["CP"] =
                #myItem["QUARTIER"] = new_dict2.get('barrio')
                #myItem["REGION"] =
                #myItem["PROVINCE"] = new_dict2.get('provincia')
                #myItem["ACHAT_LOC"] = new_dict2.get('tipoDeOperacion')#1
                #myItem["MAISON_APT"] = new_dict2.get('tipoDePropiedad')#1
                #myItem["ANNONCE_TEXT"] = response.css('span.js-flex-box.description-body ::text ').extract_first()
                #myItem["ANNONCE_TEXT"] = response.xpath('//*[@id="id-descipcion-aviso"]/text()').extract()
                #myItem["ETAGE"] =
                #myItem["NB_ETAGE"] =
                #myItem["LATITUDE"] = response.xpath('//*[@id="lat"]/@value').extract()
                #myItem["LONGITUDE"] = response.xpath('//*[@id="lng"]/@value').extract()
                #myItem["M2_TOTALE"] = all_s[7]
                #myItem["SURFACE_TERRAIN"] = all_s[4]
                #myItem["NB_GARAGE"] =
                #myItem["PIECE"] =
                
                #myItem["PRIX_M2"] =
                #myItem["URL_PROMO"] =
                #myItem["PAYS_AD"] =
                #myItem["PRO_IND"] =
                #myItem["MINI_SITE_URL"] =
                #myItem["MINI_SITE_ID"] =
                #myItem["AGENCE_ADRESSE"] =
                #myItem["FLUX"] =
                #myItem["SITE_SOCIETE_URL"] =
                #myItem["SITE_SOCIETE_ID"] =
                #myItem["SITE_SOCIETE_NAME"] =
                #myItem["AGENCE_RCS"] =
                #myItem["SPIR_ID"] =
                #myItem["AGENCE_VILLE"] =
                #myItem["EMAIL"] =
                #myItem["WEBSITE"] =
                #myItem["AGENCE_TEL"] =
                #myItem["AGENCE_TEL_2"] =
                #myItem["AGENCE_TEL_3"] =
                #myItem["AGENCE_TEL_4"] =
                #myItem["AGENCE_FAX"] =
                #myItem["AGENCE_CONTACT"] =
                #myItem["PAYS_DEALER"] =
                
                
                yield myItem







