import yaml
import parser

def process_source(browser, source):
    for new in parser.web_parser.parse(browser, source):
        print(new['timestamp'], new['content'])
        parser.object_parser.parse(new)

def main():
    new = {}
    new['timestamp'], new['content'] = None, None
    # new['content'] = "Bệnh nhân 252 là 30 tuổi, nu"
    # new['content'] = "Bệnh nhân 250 - nữ, 50 tuổi, trú tại Hạ Lôi, Mê Linh, Hà Nội. Bệnh nhân là hàng xóm và có tiếp xúc gần BN243"
    new['content'] = "BN250 - nữ, 55 tuổi, trú tại Hạ Lôi, Mê Linh, Hà Nội. Bệnh nhân là hàng xóm và có tiếp xúc gần BN243"

    if parser.object_parser.fakenew(new):
        print("Tin thật !!!!!!")
    else:
        print("Tin giả !!!")

if __name__ == '__main__':
    main()
