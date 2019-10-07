import requests
from lxml import etree
import threading
from pymongo import MongoClient
import time

class CommentsSpider():
    def __init__(self):
        self.collection = MongoClient()['text']['dbcomments']
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie':''
        }

    def get_html(self,url):
        try:
            res = requests.get(url,headers=self.headers)
            res.raise_for_status()
            return res.text
        except:
            print('获取失败')

    def parse_html(self,html):
        response = etree.HTML(html)
        comments = response.xpath("//div[@id='comments']/div")[:-2]
        for comment in comments:
            item = {}
            item['author'] = comment.xpath(".//div[@class='avatar']/a/@title")[0]
            item['votes'] = comment.xpath(".//span[@class='comment-vote']/span[@class='votes']/text()")[0]
            item['star'] = comment.xpath(".//span[@class='comment-info']/span[2]/@class")[0]
            item['time'] = comment.xpath(".//span[@class='comment-time ']/@title")[0]
            item['text'] = comment.xpath(".//span[@class='short']/text()")
            print(item)
            self.save_item(item)

    def save_item(self,item):
        self.collection.insert(item)

if __name__ == '__main__':
    id = 27622447
    nums = 128890
    base_url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P'
    comments = CommentsSpider()
    for i in range(nums//2):
        url = base_url.format(id,i*20)
        html = comments.get_html(url)
        comments.parse_html(html)
        time.sleep(5)

