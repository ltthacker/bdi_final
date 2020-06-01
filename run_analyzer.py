import util
import analyzer

def main():
    config = util.load_config()
    ssc = util.get_spark_streaming_context()

    # receive lines of data
    lines = ssc.socketTextStream('localhost', config['port'])

    # flatmap lines to list of dict
    items = lines.flatMap(util.bin2json)

    # flatmap lines to fake new class (NG, T, F)
    def analyzer_check(item):
        result = analyzer.check(item['sentence'])
        item['not_given'] = result == analyzer.NOT_GIVEN
        item['true'] = result == analyzer.TRUE
        return item
    checked_items = items.map(analyzer_check)
#    checked_items.pprint()

    # filter item with not given false, which is relevant
    # or in our knowledge domain
    def is_relevant(item):
        if not item['not_given']:
            return item
    relevant_items = checked_items.filter(is_relevant)
    relevant_items.pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()

#    item = {'url': 'https://baomoi.com/', 'sentence': "Nữ BN 278 khỏi Covid-19: 'Rất may không phải là bản sao BN 91'"}
#    result = analyzer.check(item['sentence'])
#    print('NOT_GIVEN={} TRUE={}'.format(result==analyzer.NOT_GIVEN, result==analyzer.TRUE))
