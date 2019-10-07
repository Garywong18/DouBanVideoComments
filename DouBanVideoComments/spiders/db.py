# -*- coding: utf-8 -*-
import scrapy
from DouBanVideoComments.settings import COOKIE

class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/27622447/comments?start=0&limit=20&sort=new_score&status=P']
    base_url ='https://movie.douban.com/subject/27622447/comments?start={}&limit=20&sort=new_score&status=P'

    def start_requests(self):
        cookies = {i.split('=')[0]:i.split('=')[1] for i in COOKIE.split(';')}
        for i in range(128813//20):
            url = self.base_url.format(i*20)
            yield scrapy.Request(
                url,
                cookies=cookies,
                callback=self.parse
            )
    def parse(self, response):
        comments = response.xpath("//div[@id='comments']/div")
        for comment in comments:
            item = {}
            item['author'] = comment.xpath(".//div[@class='avatar']/a/@title").extract_first()
            item['votes'] = comment.xpath(".//span[@class='comment-vote']/span[@class='votes']/text()").extract_first()
            item['star'] = comment.xpath(".//span[@class='comment-info']/span[2]/@class").extract_first()
            item['time'] = comment.xpath(".//span[@class='comment-time ']/@title").extract_first()
            item['text'] = comment.xpath(".//span[@class='short']/text()").extract()
            yield item



