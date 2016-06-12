#!/usr/bin/python
# This Python file uses the following encoding: utf-8
'''
Armenian spellchecker based on http://norvig.com/spell-correct.html
'''

import re, collections, unicodedata, codecs, operator, os, time, heapq

''' Helpers '''

def printUs(words):
    print (',').join(words)

def getSecond(x):
    if x and len(x) >= 2:
        return x[1]

def getFirst(x):
    if x and len(x) >= 1:
        return x[0]

''' Spellchecker '''

class spellchecker:
    def __init__(self):
        self.armenian = re.compile(ur'[\u0531-\u0556\u0561-\u0587]+', re.UNICODE)
        self.alphabet = [u'\u0561', u'\u0562', u'\u0563', u'\u0564',
                         u'\u0565', u'\u0566', u'\u0567', u'\u0568',
                         u'\u0569', u'\u056A', u'\u056B', u'\u056C',
                         u'\u056D', u'\u056E', u'\u056F', u'\u0570',
                         u'\u0571', u'\u0572', u'\u0573', u'\u0574',
                         u'\u0575', u'\u0576', u'\u0577', u'\u0578',
                         u'\u0579', u'\u057A', u'\u057B', u'\u057C',
                         u'\u057D', u'\u057E', u'\u057F', u'\u0580',
                         u'\u0581', u'\u0582', u'\u0583', u'\u0584',
                         u'\u0585', u'\u0586', u'\u0587']
        self.NWORDS = collections.defaultdict(lambda: 1)

    def train(self, dict_file):
        # Read in words and their counts
        f = codecs.open(dict_file, encoding='utf-8')
        f.seek(0)
        for line in f:
            if line:
                count, word = line.split()
                self.NWORDS[word] = int(count)
        f.close()

    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correctSimple(self, word, n=1):
        #word = word.decode('utf-8');
        candidates = self.known([word]) | self.known(self.edits1(word)) | self.known_edits2(word)
        return heapq.nlargest(n, candidates, key=self.NWORDS.get)

    def correct(self, word, k=1, m0=1, m1=1, m2=1):
        '''
        word: mispelled word
        n:    number of corrections returned
        m0:   weight of edit0 distance
        m1:   weight of edit1 distance
        m2:   weight of edit2 distance
        '''
        edit0 = set(filter(None, [self.addFreq(word, m0)]))
        edit1 = set(filter(None, [self.addFreq(w, m1) for w in self.known(self.edits1(word))]))
        edit2 = set(filter(None, [self.addFreq(w, m2) for w in self.known_edits2(word)]))
        candidates = edit0 | edit1 | edit2
        return [getFirst(x) for x in heapq.nlargest(k, candidates, key=getSecond)]

    def addFreq(self, word, m=1):
        if word in self.NWORDS:
            return (word, self.NWORDS[word]*m)

    def spelltest(self, tests, k=1, m0=1, m1=1, m2=1, bias=None, verbose=True):
        n, bad, unknown, start = 0, 0, 0, time.clock()
        if bias:
            for target in tests: self.NWORDS[target] += bias
        for target,wrongs in tests.items():
            for wrong in wrongs.split():
                n += 1
                ws = self.correct(wrong, k, m0, m1, m2)
                if target not in ws:
                    bad += 1
                    unknown += (target not in self.NWORDS)
                    if verbose:
                        print '%03d] %s => %s (%s); expected %s (%d)' % (
                            bad, wrong.encode('utf-8'),
                            (',').join(ws).encode('utf-8'),
                            (',').join([str(self.NWORDS[w]) for w in ws]),
                            target.encode('utf-8'),
                            self.NWORDS[target])
        return dict(bad=bad, n=n, bias=bias, perc=int(100. - 100.*bad/n),
                    unknown=unknown, secs=int(time.clock()-start))

''' Main '''

if __name__ == "__main__":
    pass
    '''
    from spellchecker import *
    sp = spellchecker()
    sp.train('words.txt')
    word = 'առաջչն'.decode('utf-8')
    printUs(sp.correct(word))
    '''
