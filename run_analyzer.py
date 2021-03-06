import util
import saver
import analyzer

def main():
    config = util.load_config()
    sc, ssc, sqlc = util.get_spark_streaming_context()

    # receive lines of data
    lines = ssc.socketTextStream('localhost', config['port'])

    # flatmap lines to list of dict
    items = lines.flatMap(util.bin2json)

    # flatmap lines to fake new class (NG, T, F)
    def analyzer_check(item):
        result = analyzer.check(item['paragraph'])
        item['not_given'] = result == analyzer.NOT_GIVEN
        item['truth'] = result == analyzer.TRUE
        return item
    checked_items = items.map(analyzer_check)
    # checked_items.pprint()

    # filter item with not given false, which is relevant
    # or in our knowledge domain
    def is_relevant(item):
        if not item['not_given']:
            del item['not_given']
            return item
    relevant_items = checked_items.filter(is_relevant)
    relevant_items.pprint()

    # save mined data
    def save_streaming_data(time, rdd):
        if not rdd.isEmpty():
            saver.save(sqlc, config, 'news', rdd)
    relevant_items.foreachRDD(save_streaming_data)

    ssc.start()
    ssc.awaitTermination()

def debug():
    paragraph = '''THÔNG BÁO VỀ CA BỆNH 313: Bệnh nhân nam, 28 tuổi, ở Yên Thành, Nghệ An. Bệnh nhân từ Dubai-UAE về Việt Nam ngày 03/5/2020 trên chuyến bay VN0088, số ghế 51K. Sau khi nhập cảnh, bệnh nhân không có triệu chứng, sức khỏe ổn định và được cách ly tại khu cách ly tập trung Ký túc xá sinh viên tỉnh Bạc Liêu. Trong đợt lấy mẫu xét nghiệm ngày 13/5 của Trung tâm Kiểm soát Bệnh tật tỉnh Bạc Liêu, bệnh nhân có kết quả xét nghiệm dương tính với SARS-CoV-2. Hiện bệnh nhân được chuyển cách ly, theo dõi tại Bệnh viện Đa khoa tỉnh Bạc Liêu.'''
    result = analyzer.check_verbose(paragraph)
    print(result)

if __name__ == '__main__':
    main()
    # debug()

