# -*- coding: utf-8 -*-
import scrapy
import re


class ClspiderSpider(scrapy.Spider):
    name = 'clspider'
    allowed_domains = ['ee.flexui.win']
    start_urls = ['http://ee.flexui.win/index.php']
    start_urls = []
    for i in range(2, 5):
        url = "https://ee.flexui.win/thread0806.php?fid=8&search=&page=%s" % i
        start_urls.append(url)

    def parse(self, response):
        note_urls = response.xpath('//tr[@class="tr3 t_one tac"]/td[1]/a/@href').extract()
        for note_url in note_urls:
            yield scrapy.Request('https://ee.flexui.win/'+note_url, callback=self.parse_note)
        pass

    def parse_note(self, response):
        img_urls = response.xpath('//div[@class="tpc_content do_not_catch"]/*/@data-src').extract()
        for img_url in img_urls:
            yield scrapy.Request(img_url, callback=self.parse_download)
        pass

    def parse_download(self, response):
        # 下载图片
        url = response.url
        # 保存的图片文件名
        title = re.findall(r'\w*.jpg', url)[0]
        # 保存图片
        with open('E:\\cl_img\\%s' % title, 'wb') as f:
            f.write(response.body)