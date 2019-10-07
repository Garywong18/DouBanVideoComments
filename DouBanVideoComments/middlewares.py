# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse



class SeleniumMiddlewares():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,10)

    def process_request(self,request,spider):
        try:
            self.browser.get(request.url)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#comments'))
            )
            return HtmlResponse(
                url=request.url,
                body=self.browser.page_source,
                request=request,
                encoding='utf-8',
                status=200
            )
        except TimeoutException:
            return HtmlResponse(
                url=request.url,
                status=500,
                request=request
            )