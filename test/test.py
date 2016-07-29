import json, time, sys, codecs, pprint
sys.path.insert(0, '../src')
from spellchecker import *

if __name__ == "__main__":
    if len(sys.argv) == 7:
        dictionary = sys.argv[1]
        filename = sys.argv[2]
        k = int(sys.argv[3])
        m0 = int(sys.argv[4])
        m1 = int(sys.argv[5])
        m2 = int(sys.argv[6])
    else:
        print "Usage: python test.py <dictionary> <test_json> <k> <m0> <m1> <m2>"
        print "Example: python test.py ../src/words.txt ./tests/test1.json 3 1000 100 1"
        sys.exit()

    # Initalize and train spellchecker
    print "Initializing spellchecker..."
    sp = spellchecker()
    sp.trainDict(dictionary)

    # Run tests
    print "Running tests..."
    test_file = codecs.open(filename, "r", encoding="utf-8")
    test_json = json.loads(test_file.read())
    print sp.spelltest(test_json, k, m0, m1, m2)
