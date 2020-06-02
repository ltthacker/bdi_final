from . import util
import random

class URLCrawlerBaomoi:

    done = []
    queue = []
    start_urls = []

    def __init__(self):
        self.set_start_urls()
        self.browser = util.Browser()

    def set_start_urls(self):
        for i in range(1, 2):
            url = 'https://baomoi.com/phong-chong-dich-covid-19/top/328/trang{}.epi'.format(i)
            self.start_urls.append(url)
            self.queue.append(url)

    def crawl(self):
        for _ in self.crawl_start_urls_child():
            yield _
        for _ in self.crawl_child():
            yield _

    def crawl_start_urls_child(self):
        for url in self.start_urls:
            for href in util.get_href(self.browser, url):
                if href not in self.done:
                    if href not in self.queue:
                        self.queue.append(href)
                        yield url, href

    def crawl_child(self):
        while 1:
            # shuffle the queue to get more diverse content
            # since the first 500 x number of start page all from 
            # baomoi.com front page
            random.shuffle(self.queue)

            # pop the news
            url = self.queue.pop(0)
            for href in util.get_href(self.browser, url, keyword='covid'):
                if href not in self.done:
                    if href not in self.queue:
                        self.queue.append(href)
                        yield url, href
            self.done.append(url)


class URLCrawlerNcov:

    done = []
    queue = []
    start_urls = []

    def __init__(self):
        self.set_start_urls()
        self.browser = util.Browser()

    def set_start_urls(self):
        for i in range(1, 2):
            url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
            self.start_urls.append(url)
            self.queue.append(url)
            self.start_urls.append(url)

    def crawl(self):
        for _ in self.crawl_start_urls_child():
            yield _
        for _ in self.crawl_child():
            yield _

    def crawl_start_urls_child(self):
        for url in self.start_urls:
            for href in util.get_href(self.browser, url):
                if href not in self.done:
                    if href not in self.queue:
                        self.queue.append(href)
                        yield url, href

    def crawl_child(self):
        while 1:
            # shuffle the queue to get more diverse content
            # since the first 500 x number of start page all from 
            # baomoi.com front page
            random.shuffle(self.queue)

            # pop the news
            url = self.queue.pop(0)
            for href in util.get_href(self.browser, url, keyword='covid'):
                if href not in self.done:
                    if href not in self.queue:
                        self.queue.append(href)
                        yield url, href
            self.done.append(url)

