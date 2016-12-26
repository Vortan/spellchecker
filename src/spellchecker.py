#!/usr/bin/python
# This Python file uses the following encoding: utf-8
'''
Armenian spellchecker based on http://norvig.com/spell-correct.html
'''

import re, collections, unicodedata, codecs, operator, os, time, heapq, termcolor, sys, pickle

''' Constants '''

# Minimum frequency for word to be considered correct
# TODO: should be input (with default)
THRESHOLD = 1e-06

# Weights
# TODO: elaborate + should also be input 
MG = 0.95
M1 = 0.04
M2 = 0.01

# Armenian unicode  alphabet
ALPHABET = [u'\u0561', u'\u0562', u'\u0563', u'\u0564',
            u'\u0565', u'\u0566', u'\u0567', u'\u0568',
            u'\u0569', u'\u056A', u'\u056B', u'\u056C',
            u'\u056D', u'\u056E', u'\u056F', u'\u0570',
            u'\u0571', u'\u0572', u'\u0573', u'\u0574',
            u'\u0575', u'\u0576', u'\u0577', u'\u0578',
            u'\u0579', u'\u057A', u'\u057B', u'\u057C',
            u'\u057D', u'\u057E', u'\u057F', u'\u0580',
            u'\u0581', u'\u0582', u'\u0583', u'\u0584',
            u'\u0585', u'\u0586', u'\u0587']

# Groupings of letters that are often mistaken for one another
''' Դ - Տ - Թ '''
d  = u'\u0564'  #դ
t  = u'\u057f'  #տ
tt = u'\u0569'  #թ
group_d = [d, tt, t]

''' Գ - Կ - Ք '''
g  = u'\u0563'  #գ
k  = u'\u056f'  #կ
kk = u'\u0584'  #ք
group_g = [g, k, kk]

''' Բ - Պ - Փ '''
b  = u'\u0562'  #բ
p  = u'\u057a'  #պ
pp = u'\u0583'  #փ
group_b = [b, p, pp]

''' Ձ - Ծ - Ց '''
dz = u'\u0571'  #ձ
c  = u'\u056e'  #ծ
ts = u'\u0581'  #ց
group_c = [dz, c, ts]

''' Ջ - Ճ - Չ '''
j  = u'\u057b'  #ջ
jj = u'\u0573'  #ճ
ch = u'\u0579'  #չ
group_j = [j, jj, ch]

''' Ղ - Խ '''
gh = u'\u0572'  #ղ
kh = u'\u056d'  #խ
group_gh = [gh, kh]

''' Ր - Ռ '''
r  = u'\u0580'  #ր
rr = u'\u057c'  #ռ
group_r = [r, rr]

''' Է - Ե '''
e  = u'\u0567'  #է
ye = u'\u0565'  #ե
group_e = [e, ye]

''' Օ - Ո '''
o  = u'\u0585'  #օ
vo = u'\u0578'  #ո
group_o = [o, vo]

GROUPS = [group_d, group_g, group_b,
          group_c, group_j, group_gh,
          group_r, group_e, group_o]

''' Trainer '''

def train(freq_filename, corr_filename=None):
    """
    Creates dictionaries out of word list files
    Returns
        freq_dict   word -> frequency probability
        corr_dict   word -> is correct bool
    """
    freq_dict = collections.defaultdict(lambda: 0.0)
    corr_dict = collections.defaultdict(bool)

    freq_file = codecs.open(freq_filename, encoding='utf-8')
    freq_file.seek(0)
    for line in freq_file:
        if line:
            word, freq = line.strip().split()
            freq_dict[word] = float(freq)

    freq_file.close()

    if corr_filename:
        corr_file = codecs.open(corr_filename, encoding='utf-8')
        corr_file.seek(0)
        for line in corr_file:
            if line:
                word = line.strip()
                corr_dict[word] = True
        corr_file.close()

    return freq_dict, corr_dict

''' Spellchecker '''

class spellchecker:
    def __init__(
        self,
        fwords,
        cwords,
        alphabet=ALPHABET,
        threshold=THRESHOLD,
        m1=M1,
        m2=M2,
        groups=GROUPS,
        mg=MG,
    ):
        """ 
        fwords      dict of word -> frequency
        cwords      dict of word -> is correct
        alphabet    unicode array of letters
        threshold   words with freq greater than
                     this are considered correct
        m1          weight of edit distance 1
        m2          weight of edit distance 2
        groups      array of arrays of letters that
                     are often mistaken for one another
        mg          weight of group replacements
        """
        self.fwords = fwords
        self.cwords = cwords
        self.alphabet = alphabet
        self.threshold = threshold
        self.m1 = m1
        self.m2 = m2
        self.groups = groups
        self.mg = mg

    def isCorrect(self, word):
        if self.cwords[word]:
            return True
        if self.fwords[word] > self.threshold:
            return True
        return False
    
    def correct(self, word, k=1):
        '''
        word    word
        k       # of corrections
        '''

        if self.isCorrect(word):
            return [word]

        candidates = {}
        def consider(w, m):
            score = self.fwords[w] * m
            if w not in candidates or score > candidates[w]:
                candidates[w] = score

        for w in self.known(self.edits1(word)): consider(w, self.m1)
        for w in self.known(self.edits2(word)): consider(w, self.m2)
        for w in self.known(self.editsG(word)): consider(w, self.mg)

        return [x for x in heapq.nlargest(k , candidates, key=lambda x: candidates[x])]

    def known(self, words): return set(w for w in words if w in self.fwords)
    
    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)
    
    def edits2(self, word):
        return set(e2 for e1 in self.edits1(word)
                        for e2 in self.edits1(e1) if e2 in  self.fwords)
   
    def editsG(self, word):
        def find(s, ch):
            return [i for i, ltr in enumerate(s) if ltr == ch]

        edits = set()
        for pair in self.groups:
            for letter in pair:
                indices = find(word, letter)
                if indices:
                    without = pair[:]
                    without.remove(letter)
                    for i in indices:
                        for w in without:
                            edits.add(word[:i] + w + word[i+1:])

        return edits

