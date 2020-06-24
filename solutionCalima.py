from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.analyzer import CalimaStarAnalyzer
import camel_tools.utils

db = CalimaStarDB('/usr/local/lib/python3.7/site-packages/camel_tools/calima_star/databases/almor-msa/almor-msa-r13.db', 'a')
analyzer = CalimaStarAnalyzer(db)

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
        analyses = analyzer.analyze(root)
        for a in analyses:
            if a['root'] == root[0]+'.'+root[1]+'.'+root[2]:
                if a['diac'][1] == 'َ' and a['diac'][3] == 'ْ':
                    return True
    elif len(word) == 3:
        root    = word[1:3]
        fa      = root[0]
        ain     = root[1]
        rootx   = root
        rootWaw = root + 'و'
        rootYa  = root + 'ي'
        analyses = analyzer.analyze(rootx)
        for a in analyses:
            if a['root'] == root[0]+'.'+root[1]+'.'+root[1]:
                return True
        analyses = analyzer.analyze(rootWaw)
        for a in analyses:
            if a['root'] == root[0]+'.'+root[1]+'.'+'و':
                if a['diac'][1] == 'َ' and a['diac'][3] == 'ْ':
                    return True
        analyses = analyzer.analyze(rootYa)
        for a in analyses:
            if a['root'] == root[0]+'.'+root[1]+'.'+'ي':
                if a['diac'][1] == 'َ' and a['diac'][3] == 'ْ':
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
    diac = diacritize(root)
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
    if isMascualine(madAlif) or isMascualine(madWaw) or isMascualine(madYa):
        return True
    return False

#فعلة
def isPP4(word):
    for pp4 in PP4S:
        if word == pp4:
            return True
    return False

def diacritize(root):
    analyses = analyzer.analyze(root)
    for a in analyses:
        if a['root'] == root[0]+'.'+root[1]+'.'+root[2]:
            return a['diac']
    return root

def isMascualine(word):
    analyses = analyzer.analyze(word)
    for a in analyses:
        if a['gen'] == 'm':
            return True
    return False

def isAdj(root):
    analyses = analyzer.analyze(root)
    for a in analyses:
        if a['root'] == root[0]+'.'+root[1]+'.'+root[2]:
            if a['pos'] == 'adj':
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

out = open("output.txt", "w+")
for word in output:
    out.write(word + "\n")
out.close()
