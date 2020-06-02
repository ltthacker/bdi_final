from .object_parser_util import getObject
from .object_parser_fakenew_util import checkObject

def parse(new):
    # new is a json contain
    # - timestamp
    # - content
    return getObject(new['content'],new['timestamp'])


def fakenew(content):
    # new is a json contain
    # - timestamp
    # - content
    return checkObject(content)
