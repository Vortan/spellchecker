#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys, os, re, unicodedata, codecs, operator, collections, time

def getWords(text):
    '''
    Match all armenian words
    pattern: armenian string
    0531 - Ա, 0556 - Ֆ, 0561 - ա, 0587 - և
    '''
    pattern = ur'[\u0531-\u0556\u0561-\u0587]+'
    armenian_word = re.compile(pattern, re.UNICODE)
    return re.findall(armenian_word, text)

def removePunc(text):
    '''
    Remove puncation
    pattern: All Armenian punctuation
    055E - QUESTION MARK    055C - EXCLAMATION MARK
    058A - HYPHEN           055B - EMPHASIS MARK
    '''
    pattern = ur'[\u055E\u055C\u058A\u055B]'
    punctuation = re.compile(pattern, re.UNICODE)
    return re.sub(punctuation, '', text)

def removeProper(text):
    '''
    Remove all words that are capital and not after punctuation
    pattern: Capitalized armenian word not after punctuation
    '''
    pattern = ur'((?<![^―:։—\n\r․…–])\s[\u0531-\u0556][\u0561-\u0587]+)'
    proper_word = re.compile(pattern, re.UNICODE)
    return re.sub(proper_word, ' ', text)

def makeDict(features):
    '''
    Make frequency dictionary
    '''
    model = collections.defaultdict(lambda: 1)
    for f in features:
      if f != None:
          model[f] += 1
    return model

def printDict(dict):
    '''
    Sort and print unicode dictionary
    '''
    s_list = sorted(dict.items(), key=operator.itemgetter(1))
    for k,v in s_list:
        print '%7d\t%s' % (v, k.encode('utf-8'))

def main():
    # Get directory
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        print "Usage: ./collector.py <dir>"
        print "Example: ./collector.py books/*.txt"

    logfile = open("log_%s.txt" % time.time(), 'w+')

    # Collect words
    words = []

    # get all .txt file paths recursively
    files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path)
    for f in files if f.endswith('.txt')]

    for filename in files:
        logfile.write(filename + "\n")
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        text = removeProper(text)
        text = removePunc(text)
        text = text.lower()
        words += getWords(text)
        f.close()
    NWORDS = makeDict(words)
    printDict(NWORDS)

if __name__ == "__main__":
    main()
