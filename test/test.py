import json, time, sys, codecs, pprint
sys.path.insert(0, '../src')
from spellchecker import *

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dictionary = sys.argv[1]
        filename = sys.argv[2]
    else:
        print "Usage: ./test.py <dictionary> <test_json>"
        print "Example: ./test.py ../str/words.txt ./tests/test1.json"

    # Initalize and train spellchecker
    print "Initializing spellchecker..."
    sp = spellchecker()
    sp.train(dictionary)

    # Run tests
    print "Running tests..."
    test_file = codecs.open(filename, "r", encoding="utf-8")
    test_json = json.loads(test_file.read())
    print sp.spelltest(test_json)
