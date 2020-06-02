from .object_parser_util import getObject
from .object_parser_fakenew_util import checkObject

def parse(new):
    return getObject(new['content'],new['timestamp'])


def fakenew(content):
    return checkObject(content)
