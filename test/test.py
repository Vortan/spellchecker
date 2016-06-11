import json, time, sys, codecs, pprint
sys.path.insert(0, '../src')
from spellchecker import *

if __name__ == "__main__":
    if len(sys.argv) == 4:
        dictionary = sys.argv[1]
        filename = sys.argv[2]
        k = int(sys.argv[3])
    else:
        print "Usage: python test.py <dictionary> <test_json> <k>"
        print "Example: python test.py ../str/words.txt ./tests/test1.json 3"
        sys.exit()

    # Initalize and train spellchecker
    print "Initializing spellchecker..."
    sp = spellchecker()
    sp.train(dictionary)

    # Run tests
    print "Running tests..."
    test_file = codecs.open(filename, "r", encoding="utf-8")
    test_json = json.loads(test_file.read())
    print sp.spelltest(test_json, k)
