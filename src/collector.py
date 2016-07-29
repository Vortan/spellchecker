#!/usr/bin/python
# This Python file uses the following encoding: utf-8
'''
collector by Souren Papazian.
Parses out and prints all Armenian words from all the files in a directory recursively.
'''

import sys, os, re, unicodedata, codecs, operator, collections, time, epub

def printProgress(i, total, ext):
    sys.stderr.write('\r')
    sys.stderr.write("Progress: {0:.1f}%".format(i/float(total) * 100) + " of '%s'" % ext)
    sys.stderr.flush()

def getWords(text):
    '''
    Match all armenian words

    pattern: armenian string

    0531 - Ա
    0556 - Ֆ
    0561 - ա
    0587 - և
    '''
    pattern = ur'[\u0531-\u0556\u0561-\u0587]+'
    armenian_word = re.compile(pattern, re.UNICODE)
    return re.findall(armenian_word, text)

def removePunc(text):
    '''
    Remove puncation (meant to removed punctuation contained inside/around a word)

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

def outputWords(words):
    for word in words:
        print word.encode('utf-8')

def processTxtFile(filename):
    txt_words = []
    try:
        f = codecs.open(filename, encoding='utf-8')
        f.seek(0)
        text = f.read()
        text = removeProper(text)
        text = removePunc(text)
        text = text.lower()
        txt_words = getWords(text)
        f.close()
    except (UnicodeDecodeError, OSError, IOError) as e:
        pass
    return txt_words

def processEpubFile(filename):
    epub_words = []
    book = epub.open_epub(filename)
    for item in book.opf.manifest.values():
        try:
            text = book.read_item(item)
        except KeyError as k:
            continue
        try:
            text = text.decode('utf-8')
        except UnicodeDecodeError as u:
            pass
        text = removeProper(text)
        text = removePunc(text)
        text = text.lower()
        epub_words += getWords(text)
    book.close()
    return epub_words

if __name__ == "__main__":
    if len(sys.argv) == 3:
        path = sys.argv[1]
        exts = sys.argv[2].split(',')
    else:
        sys.stderr.write("Usage:   ./collector.py <dir/> <extention1,extention2...>\n")
        sys.stderr.write("Example: ./collector.py .../corpus/ txt,html,epub > words.txt\n")
        sys.exit()

    # for each extention collect words
    for ext in exts:
        # get all .ext file paths recursively
        files = [os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(path)
        for f in files if f.endswith('.' + ext)]
        sys.stderr.write("Found %d '%s' files\n" % (len(files), ext))
        # for each file
        for i, filename in enumerate(files):
            words = []
            if ext == 'txt' or ext == 'html':
                words = processTxtFile(filename)
            elif ext == 'epub' or ext == 'epub_;' or 'epub' in ext:
                words = processEpubFile(filename)
            else:
                sys.stderr.write('%s not supported.' % ext)
            printProgress(i+1, len(files), ext)
            outputWords(words)
        if files: sys.stderr.write('\n')
    sys.stderr.write("done\n")
