from . import parser

NOT_GIVEN = 0
TRUE = 1
FALSE = 2

def check(sentence):
    try:
        flag = parser.object_parser.fakenew(sentence)
    except:
        return NOT_GIVEN
    else:
        if flag:
            return TRUE
        else:
            return FALSE

