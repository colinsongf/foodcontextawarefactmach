"""
Created on Sun Feb 15 22:10:07 2015

@author: ruifpmaia
"""
from __future__ import division
import numpy as np
import pandas as pd
from random import shuffle
from sklearn.cross_validation import KFold
import sys



def shuffleSplitSave(datafile, percent, idx):
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                line = line.strip()
                complete_ds.append(line)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print "Total Rating Count in Dataset " + datafile + " is " + str(total_rat_cnt)
"""
    total_cnt = len(complete_ds)
    test_cnt = percentage_to_cnt(percent, total_cnt)
    print str(percent) + "% corresponds to " + str(test_cnt) + " lines"
    test_ds = []
    train_ds = []
    print "Shuffling and splitting complete dataset into train and test datasets"
    shuffle(complete_ds)
    test_ds = complete_ds[:test_cnt]
    train_ds = complete_ds[test_cnt+1:]    
    print "Writing train dataset to txt file"
    f = open(datafile + "." + str(idx) + ".base", "w")
    f.write("\n".join(map(lambda x: str(x), train_ds)))
    f.close()
    print "Writing test dataset to txt file"
    f = open(datafile + "." + str(idx) + ".test", "w")
    f.write("\n".join(map(lambda x: str(x), test_ds)))
    f.close()
    print "Finished shuffling and splitting files"
"""
    return 1


print "python argv[] %s" % sys.argv
print "param 1: datafile, param 2: n folds, percentage param 3: iteration"
shuffleSplitSave(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    

