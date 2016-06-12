#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys, os, re, unicodedata, codecs, operator, collections, time

def printProgress(i, total):
    sys.stderr.write('\r')
    sys.stderr.write("Progress: {0:.1f}%".format(i/float(total) * 100))
    sys.stderr.flush()

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

    0559 - ARMENIAN MODIFIER LETTER LEFT HALF RING
    055A - ARMENIAN APOSTROPHE
    055B - ARMENIAN EMPHASIS MARK
    055C - ARMENIAN EXCLAMATION MARK
    055D - ARMENIAN COMMA
    055E - ARMENIAN QUESTION MARK
    055F - ARMENIAN ABBREVIATION MARK
    0589 - ARMENIAN FULL STOP
    058A - ARMENIAN HYPHEN
    00AB - LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    00BB - RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    '''
    pattern = ur'[\0559\055A\055B\055C\055E\055F\0589\058A\00AB\00BB]'
    punctuation = re.compile(pattern, re.UNICODE)
    return re.sub(punctuation, '', text)

def removeProper(text):
    '''
    Remove all words that are capital and not after fullstop punctuation
    pattern: Capitalized armenian word not after fullstop punctuation
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

if __name__ == "__main__":
    # Get directory
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        print "Usage: ./collector.py <dir>"
        print "Example: ./collector.py books/*.txt"
        sys.exit()

    #logfile = open("log_%s.txt" % time.time(), 'w+')

    # Collect words
    words = []

    # get all .txt file paths recursively
    files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path)
    for f in files if f.endswith('.txt')]

    for i, filename in enumerate(files):
        #logfile.write(filename + "\n")
        printProgress(i, len(files))
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
