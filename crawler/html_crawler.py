from . import util

class HTMLCrawler:

    def __init__(self):
        self.browser = util.Browser()

    def crawl(self, url):
        '''
        crawl a url and yield all of its sentences
        Input:
            - url (str): url that needed to be crawled
        Output:
            - item (dict): contain pair of url and sentence
        '''
        html = self.browser.get(url)
        for sentence in util.html2sentences(html):
            item = {'url': url,
                    'sentence': sentence}
            yield item
