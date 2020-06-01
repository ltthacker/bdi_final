import util
import crawler

def main():
    # initialize crawler
    print('[+] initialize url crawler')
    # url_crawler = crawler.URLCrawlerBaomoi()
    url_crawler = crawler.URLCrawlerNcov()
    print('[+] initialize html crawler')
    html_crawler = crawler.HTMLCrawler()

    # initalize socket to communicate with SparkStreaming
    print('[+] initialize server connection')
    sock, connection = util.server_get_connection()

#    # run the crawler sequentially
#    try:
#        for source_url, url in url_crawler.crawl():
#            print('[crawled] source_url:{} url:{}'.format(source_url, url))
#            for item in html_crawler.crawl(url):
#                data = util.json2bin(item)
#                connection.sendall(data)
#    except KeyboardInterrupt:
#        connection.close()
#        sock.close()

    # debug one one link only
    url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
    for item in html_crawler.crawl(url):
        data = util.json2bin(item)
        connection.sendall(data)

    connection.close()
    sock.close()

if __name__ == '__main__':
    main()
