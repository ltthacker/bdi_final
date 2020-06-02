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
            - item (dict): contain pair of url and paragraph (previously
            is sentences but that will not work, cannot parse the semantic)
        '''
        html = self.browser.get(url)
        for p in util.html2paragraphs(html):
            item = {'url': url, 'paragraph': p}
            yield item
