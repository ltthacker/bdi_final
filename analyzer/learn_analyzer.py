import yaml
import parser

def process_source(browser, source):
    for new in parser.web_parser.parse(browser, source):
        print(new['timestamp'], new['content'])
        parser.object_parser.parse(new)

def main():
    browser = parser.Browser()
    sources = yaml.load(open('source.yaml').read(), Loader=yaml.FullLoader)
    for source in sources:
        process_source(browser, source)

if __name__ == '__main__':
    main()
