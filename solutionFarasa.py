from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.analyzer import CalimaStarAnalyzer
import camel_tools.utils
import http.client
import datetime


print("Started: " + str(datetime.datetime.now()))

conn = http.client.HTTPSConnection("farasa-api.qcri.org")
headers = { 'content-type': "application/json", 'cache-control': "no-cache", }


PP4S = [
'فتية',
'صبية',
'غلمة',
'جيرة',
'إخوة',
'شيخة',
'ثيرة'
]

def isAVowel(char):
    if char == 'ا':
        return True
    if char == 'أ':
        return True
    if char == 'ي':
        return True
    if char == 'ى':
        return True
    if char == 'و':
        return True
    return False

#أفعل
def isPP1(word):
    if word[0] != 'ا' and word[0] != 'أ':
        return False
    if (len(word) == 4):
        root    = word[1:4]
        fa      = root[0]
        ain     = root[1]
        lam     = root[2]
        w = root
        payload = "{\"text\": \""+w+"\"}"
        conn.request("POST", "/msa/webapi/diacritizeV2", payload.encode('utf-8'), headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = eval(data)
        diac = data['output']
        if diac[1] == 'َ' and diac[3] == 'ْ':
            return True
    elif len(word) == 3:
        root    = word[1:3]
        fa      = root[0]
        ain     = root[1]
        rootx   = root
        rootWaw = root + 'و'
        rootYa  = root + 'ي'
        w = rootx
        payload = "{\"text\": \""+w+"\"}"
        conn.request("POST", "/msa/webapi/diacritizeV2", payload.encode('utf-8'), headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = eval(data)
        diac = data['output']
        if diac[1] == 'َ' and diac[3] == 'ْ':
            return True
        w = rootWaw
        payload = "{\"text\": \""+w+"\"}"
        conn.request("POST", "/msa/webapi/diacritizeV2", payload.encode('utf-8'), headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = eval(data)
        diac = data['output']
        if diac[1] == 'َ' and diac[3] == 'ْ':
            return True
        w = rootYa
        payload = "{\"text\": \""+w+"\"}"
        conn.request("POST", "/msa/webapi/diacritizeV2", payload.encode('utf-8'), headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = eval(data)
        diac = data['output']
        if diac[1] == 'َ' and diac[3] == 'ْ':
            return True
    return False

#أفعال
def isPP2(word):
    if (word[0] != 'ا' and word[0] != 'أ') or (word[3] != 'ا'):
        return False
    root        = word[1:3] + word[4]
    fa          = root[0]
    ain         = root[1]
    lam         = root[2]
    if not isAVowel(lam):
        return True
    if  ain == lam and ain != fa:
        return True
    if ain == 'ي' and lam == 'ء':
        return True
    w = root
    payload = "{\"text\": \""+w+"\"}"
    conn.request("POST", "/msa/webapi/diacritizeV2", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)
    diac = data['output']
    if diac[1] == 'َ' and diac[3] == 'ْ':
        return True
    if (diac[1] != 'َ' or diac[3] != 'ْ') and not isAVowel(fa) and not isAVowel(ain):
        return True
    return False

#أفعلة
def isPP3(word):
    if word[0] != 'ا' and word[0] != 'أ':
        return False
    if len(word) == 5:
        root        = word[1:4]
        fa          = root[0]
        ain         = root[1]
        lam         = root[2]
    elif len(word) == 4:
        root        = word[1:3]
        fa          = root[0]
        ain         = root[1]
        lam         = root[1]
    if lam != 'ي':
        madAlif     = fa+ain+'َ'+'ا'+lam
        madWaw      = fa+ain+'ُ'+'و'+lam
        madYa       = fa+ain+'ِ'+'ي'+lam
    else:
        madAlif     = fa+ain+'َ'+'ا'+'ء'
        madWaw      = fa+ain+'ُ'+'و'+'ء'
        madYa       = fa+ain+'ِ'+'ي'+'ء'

    w = madAlif
    payload = "{\"text\": \""+w+"\"}"
    conn.request("POST", "/msa/webapi/pos", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)
    isMascualineAlif = 'M' in data[1]['num']

    w = madWaw
    payload = "{\"text\": \""+w+"\"}"
    conn.request("POST", "/msa/webapi/pos", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)
    isMascualineWaw = 'M' in data[1]['num']

    w = madYa
    payload = "{\"text\": \""+w+"\"}"
    conn.request("POST", "/msa/webapi/pos", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)
    isMascualineYa = 'M' in data[1]['num']

    if isMascualineAlif or isMascualineWaw or isMascualineYa:
        return True
    return False

#فعلة
def isPP4(word):
    for pp4 in PP4S:
        if word == pp4:
            return True
    return False


allWords = []
with open('words.txt', 'r') as words:
    w = words.readline()
    while w:
        allWords.append(w)
        w = words.readline()

output = [None] * len(allWords)
for i,word in enumerate(allWords):
    word = word.replace("آ", "اا");
    word = word.rstrip()
    word = camel_tools.utils.dediac.dediac_ar(word)
    allWords[i] = word
    length = len(word)
    output[i] =  allWords[i] + ",0"
    if length == 3 or length == 4:
        if isPP1(word):
            output[i] = allWords[i] + ",1"
        elif isPP4(word):
            output[i] = allWords[i] + ",1"
        elif length == 4:
            if  word[3] == 'ة' or word[3] == 'ه':
                if isPP3(word):
                    output[i] =  allWords[i] + ",1"
    elif length == 5:
        if word[4] == 'ة' or word[4] == 'ه':
            if isPP3(word):
                output[i] = allWords[i] + ",1"
        elif isPP2(word):
            output[i] = allWords[i] + ",1"
    else:
        output[i] = allWords[i] + ",0"

out = open("farasaSolution.txt", "w+")
for word in output:
    out.write(word + "\n")
out.close()

print("Finished: " + str(datetime.datetime.now()))
