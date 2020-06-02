import yaml
import json
import socket
from io import StringIO
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext

def load_config():
    config = yaml.load(open('config/config.yaml').read(), Loader=yaml.FullLoader)
    return config

def client_get_socket():
    config = load_config()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', config['port']))
    return sock

def server_get_connection():
    config = load_config()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', config['port']))
    sock.listen(1)
    connection, client_address = sock.accept()
    return sock, connection

def get_spark_streaming_context():
    config = load_config()
    master = config['master']
    appname = config['appname']
    interval = config['interval']

    sc = SparkContext(master, appname)
    sc.setLogLevel(config['loglevel'])
    ssc = StreamingContext(sc, interval)
    sqlc = SQLContext(sc)
    return sc, ssc, sqlc

def json2bin(data):
    data = json.dumps(data)
    data = data + '\n'
    data = data.encode()
    return data

def bin2json(data):
    result = []
    for _ in data.split('\n'):
        result.append(json.loads(_))
    return result

