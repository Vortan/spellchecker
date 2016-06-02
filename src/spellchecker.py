#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import re, collections, unicodedata, codecs, operator, os

''' Helpers '''

# Print unicode string
def printU(text):
  print text.encode('utf-8');

# Print array of unicode strings
def printUs(texts):
  for s in texts:
    print s.encode('utf-8');

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
                self.NWORDS[word] += 1
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

    def correct(self, word):
        word = word.decode('utf-8');
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word)
        if candidates:
            return max(candidates, key=self.NWORDS.get)
        else:
            return None

    def correctMatch(self, match):
        return self.correct(match.group().encode('utf-8'))

    def correctText(self, text):
        text = text.decode('utf-8');
        return re.sub(self.armenian, self.correctMatch, text);

''' Main '''

if __name__ == "__main__":
    pass
    #sp = spellchecker()
    #sp.train('words.txt')
    #print len(sp.NWORDS)
    #print sp.correct('առաջչն')
