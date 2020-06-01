import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

class Browser:

    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0')
        driver = webdriver.Firefox(profile)
        self.driver = driver

    def get(self, url):
        driver = self.driver
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        return html

    def __del__(self):
        self.driver.close()

def source1(browser):
    base_url = 'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian?p_p_id=101_INSTANCE_iEPhEhL1XSde&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=_118_INSTANCE_IrnCPpeHzQ4m__column-1&p_p_col_count=1&_101_INSTANCE_iEPhEhL1XSde_delta=30&_101_INSTANCE_iEPhEhL1XSde_keywords=&_101_INSTANCE_iEPhEhL1XSde_advancedSearch=false&_101_INSTANCE_iEPhEhL1XSde_andOperator=true&p_r_p_564233524_resetCur=false&_101_INSTANCE_iEPhEhL1XSde_cur='

    for page_id in range(1, 11):
        # go to official ncov moh gov vn timeline
        url = '{}{}'.format(base_url, page_id)

        # get raw data
        response = browser.get(url)

        # parse html
        soup = BeautifulSoup(response, 'html.parser')

        # extract time and news
        for detail in soup.find_all('div', {'class': 'timeline-detail'}):
            head    = detail.find('h3')
            content = detail.find('p')
            new = {'timestamp': head.text, 'title': '', 'content': content.text}
            # return the news
            yield new

def source2(browser):
    # go to official ncov moh gov vn announcement
    base_url = 'https://ncov.moh.gov.vn/web/guest/chi-dao-dieu-hanh?p_p_id=101_INSTANCE_iEPhEhL1XSde&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=_118_INSTANCE_IrnCPpeHzQ4m__column-1&p_p_col_count=1&_101_INSTANCE_iEPhEhL1XSde_delta=5&_101_INSTANCE_iEPhEhL1XSde_keywords=&_101_INSTANCE_iEPhEhL1XSde_advancedSearch=false&_101_INSTANCE_iEPhEhL1XSde_andOperator=true&p_r_p_564233524_resetCur=false&_101_INSTANCE_iEPhEhL1XSde_cur='

    for page_id in range(1, 3):
        # go to official ncov moh gov vn listing of announcement with page id
        url = '{}{}'.format(base_url, page_id)

        # get raw data for the list
        response = browser.get(url)

        # parse html
        soup = BeautifulSoup(response, 'html.parser')

        # extract time and title
        for item in soup.find_all('div', {'class': 'row mb-15'}):
            time    = item.find('small', {'class': 'text-muted'})
            title   = item.find('a', {'class': 'text-tletin'})
            content = item.find('description')
            new = {'timestamp': time.text, 'title': title.text, 'content': content.text}
            # return the news
            yield new

def parse(browser, source):
    news = globals()[source['name']](browser)
    return news

