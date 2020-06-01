#! /usr/bin/python3
# -*- coding: utf-8 -*-
import underthesea
import re
from . import neo4j_util as neo4j
import json


FEMALE = [r"(n|N)ữ"]
MALE = [r"(n|N)am", "nam giới"]
AGE = [r"[0-9]{1,3}\s{1,6}tuổi"]
BN_RANGE = [r"CA BỆNH\s{1,6}[0-9]{1,3} - [0-9]{1,3}",
        r"Bệnh nhân\s[0-9]{1,3} - [0-9]{1,3}",
         r"Bệnh nhân số\s{1,6}[0-9]{1,3} - [0-9]{1,3}"
       ]
BNre = [r"CA BỆNH\s{1,6}[0-9]{1,3}",
        r"(b|B)ệnh nhân\s[0-9]{1,3}",
         r"(b|B)ệnh nhân số\s{1,6}[0-9]{1,3}",
        r"BN\s{0,2}[0-9]{1,3}"
       ]
FLIGHT_RE= [r"(c|C)huyến bay\s{0,6}[A-Z]{1,4}\s?[0-9]{2,8}"]
NATIONLATY_RE = ["quốc tịch(.{0,1}[A-Z]\w{1,7}){1,3}",
                "quốc tịch(.{0,1}\w{1,7}){1,3}"]
ORIGIN = [r"(địa\s{1,2}chỉ|trú)\s{1,2}(tại|ở)\s{1,2}(\s|\w|,|TP.)*([A-Z]\w{1,})",
r"(địa chỉ|trú|quê) (tại|ở)?(\s(phường|quận|thị xã|thị trấn|tỉnh|thành phố)?(\s?\w{1,4}){1,3})"]
NUMBERSIT = ["số ghế [0-9]{1,8}[A-Z]{1,4}\s?"]
flags=re.I|re.U  
NEGATIVE_COVID = [r"(đã)?\s{1,3}(khỏi bệnh)"
]
    
def getStatus(text):
    for i in NEGATIVE_COVID:
    #         print("Regex:", i)
        result = re.search(i, text,flags)
    if result:
        return "negative"
    for i in DEATH:
#         print("Regex:", i)
        result = re.search(i, text,flags)
    if result:
        return "death"
    
    return None
def getSex(text):
    for i in FEMALE:
#         print("Regex:", i)
        result = re.search(i, text)
        if result:
            return "female"
    for i in MALE:
#         print("Regex:", i)
        result = re.search(i, text)
        if result:
            return "male"
    return None

def getAge(text):

    for i in AGE:
#         print("Regex:", i)
        result = re.search(i, text)
        if result:
            return re.findall(i, text)[0]
    return None

def BNrange(text):

    BNids = None
    for i in BN_RANGE:
    #     print("Regex:", i)
        result = re.search(i, text)
        if result:
            BNids = re.findall(i, text)[0]
            ids = re.findall(r"[0-9]{1,3}", BNids)
            return(ids)
            break
        return None

def getBNid(text):
    BNs=[]
    for i in BNre:
#         print(i)
        result = re.search(i, text)
        if result:
            text_include = re.findall(i, text)
            for bn in text_include:
                BNs.append(re.findall(r"[0-9]{1,3}", bn)[0])
    return ["BN"+BNid for BNid in BNs]


def preprocessIDBN(text):
    BNs=[]
    for i in BNre:
#         print(i)
        result = re.search(i, text)
        
        if result:
            print(result.group(0))
            text_include = re.findall(i, text,flags)
            for bn in text_include:
                print(bn)
                print(str(re.findall(r"[0-9]{1,3}", bn,flags)))
                # text = text.replace(bn,"BN"+str(re.findall(r"[0-9]{1,3}", bn)[0]))

#     BNs = set(BNs)
    text = text.replace("TP. ", "thành phố ")
    return text

def match_new(original, need_check):
    if original == need_check:
        return (True, original, need_check)
    else:
        return (False, original, need_check)
def matchInfoBN(BNid, type, value_needcheck):
    try:
        return (match_new(neo4j.getInfoBN(BNid, type), value_needcheck))
    except Exception as e:
        print("match error:",e, BNid, type, value_needcheck)
def seperateSentences(text):
    sentences = []
    for sentence in text.split('.'):
        sentences += sentence.split(";")
    return sentences
def checkRelation(text):
#     print(text)
    NEW_FLAG = []
    BNids = getBNid(text)
    BNid_main = BNids[0]

    for sentence in seperateSentences(text):
        if len(sentence) < 4:
            continue
        BNids = getBNid(sentence)
#         print(sentence)
        if len(BNids) < 2:
            continue
        else:
            for i in range(len(BNids)-1):
                BNid1 = BNids[i]
                BNid2 = BNids[i+1]
                if BNid1 == BNid2:
                    continue
                else:
                    sub = text[text.rfind(BNid1)+len(BNid1):text.find(BNid2)]
                    print(sub)
                    if "," in sub:
                        BNid1 = BNid_main
                    else:
                        BNid_main = BNid1
                    relation = sub[sub.rfind(",")+1:]
                    if relation == None:
                        relation = sub[sub.rfind("(")+1:]
                    if relation == None:
                        relation = sub
                    print("Relation:",BNid1, relation, BNid2)
                    NEW_FLAG.append(match_new(neo4j.getRelationBN(BNid1, BNid2), relation))
                    # neo4j.createConnect(BNid1, relation, BNid2)
    return NEW_FLAG

def getNationlaty(text):
    for i in NATIONLATY_RE:
        result = re.search(i, text, flags)     
        if result:
            match_obj_country = re.search("([A-Z]\w{1,7}.{0,1}){1,3}",result.group(0))
            if match_obj_country:
                return match_obj_country.group(0)
            else:
                return result.group(0)
def getOrigin(text):
    for i in ORIGIN:
        result = re.search(i, text, flags)     
        if result:
            return result.group(0)
def getFlight(text):
    for i in FLIGHT_RE:
        result = re.search(i, text)
        if result:
            return result.group(0)
    return None
def getNumberSit(text):
    for i in NUMBERSIT:
        result = re.search(i, text)
        if result:
            return result.group(0)
    return None

def processCheck(text, date=None):
    IS_TRUE_NEW = []
    BNid_main = None
    # print(1)
    for sentence in seperateSentences(text):
        print("#"*32)
        print("Sentences:",sentence)
        BNids = getBNid(sentence)
        if len(BNids) != 0:
            BNid_main = BNids[0]
        print(BNid_main)
        if date:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "date", date))
        sex = getSex(sentence)
        if sex != None:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "sex", sex))
        age = getAge(sentence)
        if age != None:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "age", age))
        flight = getFlight(sentence)
        if flight != None:
            original_flight = neo4j.getTranspotation(BNid_main)
            if original_flight == flight:
                IS_TRUE_NEW.append((True, original_flight, flight))
            else:
                IS_TRUE_NEW.append((False, original_flight, flight))
        nationlaty = getNationlaty(sentence)
        if nationlaty != None:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "nationlaty", nationlaty))

        origin = getOrigin(sentence)
        if origin != None:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "origin", origin))

        status = getStatus(sentence)
        if status != None:
            IS_TRUE_NEW.append(matchInfoBN(BNid_main, "status", status))

    return IS_TRUE_NEW
def checkObject(text, date=None):
    IS_TRUE_NEW = []
    text = preprocessIDBN(text)
    IS_TRUE_NEW += checkRelation(text)
    IS_TRUE_NEW += processCheck(text, date)
    print(json.dumps(IS_TRUE_NEW, indent=4))
    flag = True
    for i in IS_TRUE_NEW:
        flag = flag * i[0]
        print(i)
    return flag

