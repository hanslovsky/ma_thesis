#!/usr/bin/python2

import numpy as np

def prec(tp, fp):
    return tp/float(tp+fp)

def recall(tp, fn):
    return tp/float(tp+fn)

def fscore(tp, fp, fn):
    p = prec(tp, fp)
    r = recall(tp, fn)
    return 2.0*p*r/(1.0*p+r)


if __name__ == "__main__":
    # moves: all false == false
    tp = 256 + 300
    fp = 17
    fn = 61
    print "Moves (all false == false):"
    print "\t precision =", prec(tp,fp)
    print "\t recall    =", recall(tp,fn)
    print "\t fscore    =", fscore(tp, fp, fn)

    # moves: false because of size == true
    tp = 256 + 300 + 3 + 9 + 3 + 2
    fp = 12
    fn = 49
    print "Moves (false because of size == false):"
    print "\t precision =", prec(tp,fp)
    print "\t recall    =", recall(tp,fn)
    print "\t fscore    =", fscore(tp, fp, fn)

    # divisions all false == false
    tp = 53 + 36
    fp = 47
    fn = 47
    print "Divisions (all false == false):"
    print "\t precision =", prec(tp,fp)
    print "\t recall    =", recall(tp,fn)
    print "\t fscore    =", fscore(tp, fp, fn)

    # divisions timeshift false == true
    tp = 53 + 36 + 18 + 30
    fp = 17
    fn = 29
    print "Divisions (timeshift false == false):"
    print "\t precision =", prec(tp,fp)
    print "\t recall    =", recall(tp,fn)
    print "\t fscore    =", fscore(tp, fp, fn)
    
