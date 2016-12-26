import json, time, sys, codecs, pprint, argparse
sys.path.insert(0, '../src')
from spellchecker import *

parser = argparse.ArgumentParser(description='Vortan spellchecker tester')
parser.add_argument('test_filename', type=str, help="Test json file")
parser.add_argument('freq_filename', type=str, help="Frequency dictionary file")
parser.add_argument('corr_filename', type=str, help="Correct words dictionary file")
parser.add_argument('--k', type=int, help="Number of suggestions", default=3)
parser.add_argument('--m1', type=float, help="Edit distance 1 weight", default=0.04)
parser.add_argument('--m2', type=float, help="Edit distance 2 weight", default=0.01)
parser.add_argument('--mG', type=float, help="Group replacement weight", default=0.95)
parser.add_argument('--thresh', type=float, help="Min freq for word to be considered correct", default=1e-06)
parser.add_argument('--v', action='store_true', help="Print out corrections")

def spelltest(sp, tests, k, verbose=False, bias=None):
    n, bad, unknown, start = 0, 0, 0, time.clock()
    if bias:
        for target in tests: sp.fwords[target] += bias
    for target,wrongs in tests.items():
        for wrong in wrongs.split():
            n += 1
            ws = sp.correct(wrong, k)
            if target not in ws:
                bad += 1
                unknown += (target not in sp.fwords)
                if verbose:
                    print '%s\t%s => %s (%s); expected %s (%.10f)' % (
                        '-',
                        wrong.encode('utf-8'),
                        (',').join(ws).encode('utf-8'),
                        (',').join([str(sp.fwords[w]) for w in ws]),
                        target.encode('utf-8'),
                        sp.fwords[target]
                    )
            else:
                if verbose:
                    print '%s\t%s' % ('+', target)
    return dict(bad=bad, n=n, bias=bias, perc=int(100. - 100.*bad/n),
                unknown=unknown, secs=int(time.clock()-start))


if __name__ == "__main__":
    args = parser.parse_args()

    print "Training..."
    freq_dict, corr_dict = train(args.freq_filename, args.corr_filename) 

    print "Initializing spellchecker..."
    sp = spellchecker(
        fwords=freq_dict,
        cwords=corr_dict,
        threshold=args.thresh,
        m1=args.m1,
        m2=args.m2,
        mg=args.mG
    )

    print "Loading test file..."
    test_file = codecs.open(args.test_filename, "r", encoding="utf-8")
    test_json = json.loads(test_file.read())

    print "Running tests..."
    results = spelltest(sp, test_json, args.k, args.v)
    print results

