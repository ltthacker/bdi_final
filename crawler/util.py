import re
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from urllib.parse import urlparse, urljoin, ParseResult

class Browser:

    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0')
        driver = webdriver.Firefox(profile)
        self.driver = driver

    def get(self, url):
        driver = self.driver
        driver.get(url)
        html = driver.page_source
        return html

    def __del__(self):
        self.driver.close()

def is_url(url):
    r = urlparse(url)
    if len(r.scheme) > 0 and len(r.netloc) > 0:
        return True
    return False

def get_base_url(url):
    r = urlparse(url)
    r = ParseResult(r.scheme, r.netloc, '', '', '', '')
    base_url = r.geturl()
    return base_url

def get_href(browser, url, keyword=None):
    content = browser.get(url)
    base_url = get_base_url(url)
    soup = BeautifulSoup(content, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        if not is_url(href):
            href = urljoin(base_url, href)
        # filter title having keyword
        if keyword is not None:
            if keyword in a.text.lower():
                yield href
        else:
            yield href

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text2sentences(text):
    pattern = r'[^\.]+'
    for sentence in re.findall(pattern, text):
        yield sentence

def heuristic_is_sentence(sentence):
    if len(sentence.split(' ')) > 5:
        return True
    return False

def html2sentences(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    for t in filter(tag_visible, texts):
        # strip space from text
        text = t.strip()
        # extract sentences from text
        for sentence in text2sentences(text):
            if heuristic_is_sentence(sentence):
                yield sentence

def html2paragraphs(html):
    soup = BeautifulSoup(html, 'html.parser')
    ps = soup.findAll(text=True)
    for p in filter(tag_visible, ps):
        p = p.strip()
        if heuristic_is_sentence(p):
            yield p
