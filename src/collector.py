#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys, os, re, unicodedata, codecs, operator, collections, glob

def getWords(text):
    '''
    Match all Armenian words
    '''
    # All Armenian words: 0531 - Ա, 0556 - Ֆ, 0561 - ա, 0587 - և
    armenian_word = re.compile(ur'[\u0531-\u0556\u0561-\u0587]+', re.UNICODE)
    return re.findall(armenian_word, text)

def removePunc(text):
    '''
    Remove puncation
    '''
    # All Armenian punctuation: 055E - QUESTION MARK, 055C - EXCLAMATION MARK, 058A - HYPHEN, 055B - EMPHASIS MARK
    punctuation = re.compile(ur'[\u055E\u055C\u058A\u055B]', re.UNICODE)
    return re.sub(punctuation, '', text)

def removeProper(text):
    '''
    Remove all words that are capital and not after punctuation
    '''
    # Capital Armenian word not after punctuation
    proper_word = re.compile(ur'((?<![^―:։—\n\r․…–])\s[\u0531-\u0556][\u0561-\u0587]+)', re.UNICODE)
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
        print '{0:5d}\t{1}'.format(v, k.encode('utf-8'))

def main():
    # Get directory
    if len(sys.argv) == 2:
        directory = sys.argv[1]
        print directory
    else:
        print "Usage: ./collector.py <dir>"
        print "Example: ./collector.py books/*.txt"

    # Collect words
    words = []
    for filename in glob.glob(directory):
        print filename
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        text = removeProper(text)
        text = removePunc(text)
        text = text.lower()
        words += getWords(text)
    NWORDS = makeDict(words)
    printDict(NWORDS)

if __name__ == "__main__":
    main()
