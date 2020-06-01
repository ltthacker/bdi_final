#! /usr/bin/python3
# -*- coding: utf-8 -*-
# import underthesea
import re
from . import neo4j_util as neo4j
# import neo4j_util as neo4j



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
DEATH = [r"(đã)?\s{1,3}(chết|khuất|ngoẻo|tử vong|mất)",
        r"(đã)\s{1,3}(khuất|mất)"
]
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
            text_include = re.findall(i, text)
            for bn in text_include:
                text = text.replace(bn,"BN"+str(re.findall(r"[0-9]{1,3}", bn)[0]))

#     BNs = set(BNs)
    text = text.replace("TP. ", "thành phố ")
    return text


def seperateSentences(text):
    sentences = []
    for sentence in text.split('.'):
        sentences += sentence.split(";")
    return sentences
def getRelation(text):
#     print(text)
    
    BNids = getBNid(text)
    for BNid in BNids:
        neo4j.createBN(BNid,None, None, None, None, None, None, None, None)
    if len(BNids) < 2:
        return
    
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
                    neo4j.createConnect(BNid1, relation, BNid2)




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

def process(text, date=None):
    BNid_main = None
    for sentence in seperateSentences(text):
        print("#"*32)
        print("Sentences:",sentence)
        BNids = getBNid(sentence)
        if len(BNids) != 0:
            BNid_main = BNids[0]
        print(BNid_main)
        if date:
            neo4j.updateBN(BNid_main, "date", date)
        sex = getSex(sentence)
        if sex != None:
            neo4j.updateBN(BNid_main, "sex", sex)
            print("Sex:",sex)
        age = getAge(sentence)
        if age != None:
            neo4j.updateBN(BNid_main, "age", age)
            print("Age:",age)
        flight = getFlight(sentence)
        if flight != None:
            neo4j.createTranspotation(BNid_main, flight)
            print("Flight:",flight)
            numbersit = getNumberSit(sentence)
            if numbersit != None:
                neo4j.updateBN(BNid_main, "number_sit", numbersit)
                print("Numbersit:",numbersit)
                neo4j.createConnectPTVT(BNid_main, numbersit, flight)
        nationlaty = getNationlaty(sentence)
        if nationlaty != None:
            neo4j.updateBN(BNid_main, "nationlaty", nationlaty)
            print("Nation:",nationlaty)
        origin = getOrigin(sentence)
        if origin != None:
            neo4j.updateBN(BNid_main, "origin", origin)
            print("Origin:",origin)
        status = getStatus(sentence)
        if status != None:
            neo4j.updateBN(BNid_main, "status", status)
            print("Status:",status)
def getObject(text, date=None):
    try:
        text = preprocessIDBN(text)
        getRelation(text)
        process(text, date)
    except Exception as e:
        print("Error: ",e)
text = """THÔNG BÁO 7 CA BỆNH MỚI SỐ 107-113: BN107: nữ, 25 tuổi,đã chết, quốc tịch Việt Nam, nhân viên thiết kế đồ họa, là con gái và sống cùng BN86. 
Có địa chỉ thường trú tại Thanh Xuân, Hà Nội; BN108: nam, 19 tuổi, quốc tịch Việt Nam, địa chỉ ở Cầu Giấy, Hà Nội. 
    Bệnh nhân là du học sinh Việt Nam tại Anh về nước ngày 18/3 trên chuyến bay VN054; BN109: nam, 42 tuổi, quốc tịch Việt Nam, địa chỉ ở Hoàng Mai, Hà Nội. 
        Bệnh nhân là giảng viên một trường đại học của Anh, về nước ngày 15/3/2020 trên chuyến bay TG 560, số ghế 37E; BN110: nữ, 19 tuổi, quốc tịch Việt Nam, địa chỉ ở Đống Đa, Hà Nội. 
            Bệnh nhân là du học sinh tại Mỹ, hy sinh tạitại Việt Nam ngày 19/03/2020 trên chuyến bay JL751, số ghế 1A; BN111: nữ, 25 tuổi, quốc tịch Việt Nam, địa chỉ ở Hải Hậu, Nam Định. 
                Bệnh nhân là du học sinh tại Pháp, về Việt Nam ngày 18/03/2020 trên chuyến bay VN018, số ghế 36D; BN112: nữ, 30 tuổi, quốc tịch Việt Nam, địa chỉ ở Hoàn Kiếm, Hà Nội. 
Bệnh nhân là du học sinh tại Pháp đã khuất. Ngày 17/3/2020 về Việt Nam trên chuyến bay VN018;
BN113: nữ, 18 tuổi, đã khỏi bệnh ,quốc tịch Việt Nam, địa chỉ ở Hoàn Kiếm, Hà Nội. Bệnh nhân đã ngoẻo là du học sinh người Anh về nước trên chuyến bay VN054 (số ghế 2A) ngày 18/03/2020.
    Hiện tại tất cả các bệnh nhân đang được cách ly và điều trị tại Bệnh viện Bệnh nhiệt đới Trung ương cơ sở Đông Anh."""
getObject(text, "21/3")







