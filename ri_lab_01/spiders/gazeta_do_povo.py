# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

import pdb
# scrapy shell ./quotes-mapa.html 
# response.css('.conteudo-mapa a').get()

class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []


    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        response.css('.linha ').getall()
        

        for elem in response.css('dd'):
            
            link = elem.css('a::attr(href)').get()

            yield response.follow(link, callback=self.page_parse)
    
    def page_parse(self, response):
        
        session_news = response.css('.coluna1-2')
        for news_item in session_news:
            # pdb.set_trace()
            news_link = news_item.css('article > a::attr(href)').get()
            news_date = news_item.css('article > a::attr(data-publication)').get()
            news_section = news_item.css('article > a::attr(data-section)').get()
            yield response.follow(news_link, callback=self.news_parse)
            
    
    def news_parse(self, response):
        pdb.set_trace()
        dic = {}
        title = response.css('h1.col-8.c-left.c-title::text').get()
        if not title:
            title = response.css('h1.c-titulo::text').get()
            date = response.css('div.c-creditos time::text').getall()
            author = response.css('div.c-autor > span::text').get()
        else:
            subtitle = response.css('h2.c-sumario::text').get()
            author = response.css('div.item-name > span::text').get()
        
        text = ' '.join(response.css('div.gp-coluna.col-6.texto-materia.paywall-google p::text').getall())


        dictionnaire = {'title': title, 'date': date, 'author': author, 'text:' text}

        
        
        #
        #
        #
