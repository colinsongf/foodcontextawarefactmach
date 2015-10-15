"""
Created on Sun Feb 15 22:10:07 2015

@author: ruifpmaia
"""
from __future__ import division
from sklearn.cross_validation import KFold
from random import shuffle
import numpy as np
import pandas as pd

SEP_CHAR = '\t'
AVG_USER = 1
STD_USER = 2
AVG_STD_USER = 3
AVG_ITEM = 1
STD_ITEM = 2
AVG_STD_ITEM = 3


#==============================================================================
# Calculates the percentage correspondent number from total
#==============================================================================
def percentage_to_cnt(perc, total):
    return (int)((perc/100) * total)

#==============================================================================
# Receive a datafile (complete path). Calculates the number of entries 
# that correspond to the percent input parameter (taking into account the total
# number of entries in dataset) and uses idx to mark the file name just
# before extension. Generates a train and a test file.
#==============================================================================
def shuffleSplitSave(datafile, percent, idx):
    print "Datafile:%s" % datafile
    print "Percent:%d" % percent
    print "Start FileNameNumbering:%d" % idx
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
    return 1

def splitKFoldSave2(datafile, nFolds, out_filename):
    print "Datafile:%s" % datafile
    print "Number of Folds:%d" % nFolds
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
    except MemoryError:
        print "Error on line %d" % total_rat_cnt
        raise
    print "Total Rating Count in Dataset " + datafile + " is " + str(total_rat_cnt)
    kf = KFold(total_rat_cnt, n_folds=nFolds, shuffle=True, random_state=1)
    idx = 1
    print "Fold lenght: " + str(len(kf))
    # for each fold... save output data files
    for train, test in kf:    
        test_fold = []
        train_fold = [] 
        # Adding entries to train dataset
        for entry_idx in train:
            #add row to result
            train_fold.append(complete_ds[entry_idx])
        # Adding entries to test dataset
        for entry_idx in test:
            test_fold.append(complete_ds[entry_idx])
        print "Writing train dataset to txt file"
        f = open(out_filename + "." + str(idx) + ".base", "w")    
        f.write("\n".join(map(lambda x: x, train_fold)))
        f.close()
        print "Writing test dataset to txt file"
        f = open(out_filename + "." + str(idx) + ".test", "w")
        f.write("\n".join(map(lambda x: x, test_fold)))
        f.close()
        idx += 1 
    print "Finished shuffling and splitting files in %d Folds" % nFolds
    return 1
 
#==============================================================================
# Receives a dataset and the number of Folds, and generate nFolds 
# output datasets, base+test files, according to the kFold cross validation
# principle.
# Generates files with or without AVG, STD for user and item
# Receives the next free id so that it can generates correct libSVM files
#==============================================================================
def splitKFoldSave(directory, datafile, next_free_id, nFolds, avgUser, avgItem, out_filename):
    print "Datafile:%s" % datafile
    print "Number of Folds:%d" % nFolds
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(directory+datafile) as f:
            for line in f:
                line = line.strip()
                complete_ds.append(line)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    except MemoryError:
        print "Error on line %d" % total_rat_cnt
        raise
    print "Total Rating Count in Dataset " + datafile + " is " + str(total_rat_cnt)
    kf = KFold(total_rat_cnt, n_folds=nFolds, shuffle=True, random_state=1)
    idx = 1
    print "Fold lenght: " + str(len(kf))
    # for each fold... save output data files
    for train, test in kf:    
        test_fold = []
        train_fold = [] 
        user_dic = {}
        item_dic = {}
        # Adding entries to train dataset
        for entry_idx in train:
            #add row to result
            rate_evt = complete_ds[entry_idx].split(SEP_CHAR)
            train_fold.append(rate_evt)
            # for each item in rating event: sum the target and increment count
            item = item_dic.get(rate_evt[2], 0)
            # if null (item not in dictionary), initialize
            if (item == 0):
                item_dic[rate_evt[2]] = {'count':1, 'total': int(rate_evt[0]), 'events': [int(rate_evt[0])]} 
            else:
                # update dictionary
                item_dic[rate_evt[2]]['count'] += 1
                item_dic[rate_evt[2]]['total'] += int(rate_evt[0]) 
                item_dic[rate_evt[2]]['events'].append(int(rate_evt[0]))
            # for each user in rating event: sum the target and increment count
            user = user_dic.get(rate_evt[1], 0)
            if (user == 0):
                user_dic[rate_evt[1]] = {'count':1, 'total': int(rate_evt[0]), 'events': [int(rate_evt[0])]} 
            else:
                # update dictionary
                user_dic[rate_evt[1]]['count'] += 1
                user_dic[rate_evt[1]]['total'] += int(rate_evt[0]) 
                user_dic[rate_evt[1]]['events'].append(int(rate_evt[0]))
        # Adding entries to test dataset
        for entry_idx in test:
            test_fold.append(complete_ds[entry_idx].split(SEP_CHAR))
        ################################################
        # Calculate average rating of each user 
        ################################################
        for key, entry in user_dic.items():
            entry['avg'] = np.average(entry['events'])
            entry['std'] = np.std(entry['events'])
        ################################################
        # Calculate average rating of each item
        ################################################           
        for key, entry in item_dic.items():
            entry['avg'] = np.average(entry['events'])
            entry['std'] = np.std(entry['events'])
           
        ################################################            
        # Get IDX for user-avg user-std item-avg item-std
        ################################################
        user_avg_fid = str(next_free_id)
        user_std_fid = str(next_free_id +1)
        item_avg_fid = str(next_free_id +2)
        item_std_fid = str(next_free_id +3)
        ################################################
        # Calculate average rating of each user 
        ################################################
        if (avgUser == 1 or avgUser == 2 or avgUser == 3):
            for key, entry in user_dic.items():
                entry['avg'] = np.average(entry['events'])
                entry['std'] = np.std(entry['events'])
            # add user average in base training file
            for index, entry in enumerate(train_fold):
                if (avgUser == 1 or avgUser == 3):
                    entry.append(user_avg_fid + ':' + str(user_dic[entry[1]]['avg']))
                if (avgUser == 2 or avgUser == 3):
                    entry.append(user_std_fid + ':' + str(user_dic[entry[1]]['std']))
            # add user average to test file
            for index, entry in enumerate(test_fold):
                if (avgUser == 1 or avgUser == 3):
                    if entry[1] in user_dic:
                        entry.append(user_avg_fid + ':' + str(user_dic[entry[1]]['avg']))
                    else:
                        entry.append(user_avg_fid + ':' + str(entry[0]))   
                if (avgUser == 2 or avgUser == 3):
                    if entry[1] in user_dic:
                        entry.append(user_std_fid + ':' + str(user_dic[entry[1]]['std']))   
        ################################################
        # Calculate average rating of each item
        ################################################           
        if (avgItem == 1 or avgItem == 2 or avgItem == 3):
            for key, entry in item_dic.items():
                entry['avg'] = np.average(entry['events'])
                entry['std'] = np.std(entry['events'])
            # add item average in base training file
            for index, entry in enumerate(train_fold):
                if (avgItem == 1 or avgItem == 3):
                    entry.append(item_avg_fid + ':' + str(item_dic[entry[2]]['avg']))
                if (avgItem == 2 or avgItem == 3):
                    entry.append(item_std_fid + ':' + str(item_dic[entry[2]]['std']))
            # add item average to test file
            for index, entry in enumerate(test_fold):
                if (avgItem == 1 or avgItem == 3):
                    if entry[2] in item_dic:
                       entry.append(item_avg_fid + ':' + str(item_dic[entry[2]]['avg']))  
                    else:
                        entry.append(item_avg_fid + ':' + str(entry[0]))        
                if (avgItem == 2 or avgItem == 3):
                    if entry[2] in item_dic:
                       entry.append(item_std_fid + ':' + str(item_dic[entry[2]]['std']))  
        print "Writing train dataset to txt file"
        f = open(directory+out_filename + "." + str(idx) + ".base", "w")    
        f.write("\n".join(map(lambda x: SEP_CHAR.join(x), train_fold)))
        f.close()
        print "Writing test dataset to txt file"
        f = open(directory+out_filename + "." + str(idx) + ".test", "w")
        f.write("\n".join(map(lambda x: SEP_CHAR.join(x), test_fold)))
        f.close()
        idx += 1 
    print "Finished shuffling and splitting files in %d Folds" % nFolds
    return 1

#==============================================================================
# Adds the user rating event count to all the datafile folds
#==============================================================================
def addUserRatingCount(datafile, nFolds):   
    try:
        for x in range(1,nFolds+1):
            user_dic = {}
            base_fl = []
            test_fl = []
            base_fn = datafile + "." + str(x) + ".base.libfm"
            test_fn = datafile + "." + str(x) + ".test.libfm"
            #######################################################
            # Write user rating event count to train files
            #######################################################
            print 'Calculating user rating count on %s' % base_fn
            with open(base_fn) as f:
                for i, line in enumerate(f):       
                    base_fl.append(line)
                    #add row to result
                    rate_evt = line.split(SEP_CHAR)
                    # for each user in rating event: sum the target and increment count
                    user = user_dic.get(rate_evt[1], 0)
                    if (user == 0):
                        user_dic[rate_evt[1]] = {'count':1} 
                    else:
                        # update dictionary
                        user_dic[rate_evt[1]]['count'] += 1
                f.close()
            # add item average in base training file        
            for i, line in enumerate(base_fl): 
                rate_evt = line.split(SEP_CHAR)
                user = user_dic.get(rate_evt[1], 0)
                base_fl[i]=base_fl[i].strip()
                if (user == 0):
                    base_fl[i] += SEP_CHAR + '128778:1'
                else:                    
                    base_fl[i] += SEP_CHAR + '128778:' + str(user_dic[rate_evt[1]]['count'])
            print "Writing train dataset to file"
            f = open(base_fn, "w")    
            f.write("\n".join(base_fl))
            f.close()
            #######################################################
            # Write user rating event count to test files
            #######################################################
            print 'Calculating user rating count on %s' % test_fn
            with open(test_fn) as f:
                for i, line in enumerate(f):       
                    test_fl.append(line)            
            # add item average in base training file        
            for i, line in enumerate(test_fl): 
                rate_evt = line.split(SEP_CHAR)
                user = user_dic.get(rate_evt[1], 0)
                test_fl[i]=test_fl[i].strip()
                if (user == 0):
                    test_fl[i] += SEP_CHAR + '128778:1'
                else:
                    test_fl[i] += SEP_CHAR + '128778:' + str(user_dic[rate_evt[1]]['count'])
            print "Writing test dataset to file"
            f = open(test_fn, "w")    
            f.write("\n".join(test_fl))
            f.close()            
    except ValueError:
        print "Error on line [%s]" % i
        raise 
    except IndexError:
        print "Error on line [%s]" % i
        raise 
    return 1

#==============================================================================
# Receives a dataset and ovewrites it cutting the original file to a 
# count (input parameter) number of entries
#==============================================================================
def cutSave(datafile, count):
    print "Datafile:%s" % datafile
    print "Final Count:%d" % count
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                line = line.strip()
                complete_ds.append(line)        
                total_rat_cnt += 1          
        f.close()
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print "Total Rating Count in Dataset " + datafile + " is " + str(total_rat_cnt)
    print "Shuffling and cutting complete dataset to a total of %d lines" % count
    shuffle(complete_ds)
    final_ds = complete_ds[:count]    
    print "Writing train dataset to txt file"
    f = open(datafile, "w")
    f.write("\n".join(map(lambda x: str(x), final_ds)))
    f.close()
    print "Finished shuffling and cutting file"
    return 1

#==============================================================================
# Removes Epicurious Wrong Averages and Variances
#==============================================================================           
def removeWrongEpicuriousValues(ds_filename):        
    filtered_ds = []
    try:
        with open(ds_filename) as f:
            for line in f:
                st_idx = line.index(SEP_CHAR+"23852:")
                line = line.replace(' ', '\t')
                filtered_ds.append(line[:st_idx])           
        f.close()
    except IOError:
        print "Error opening file %s" % ds_filename
        raise
    except ValueError:
        print "File[%s]ERROR::Could not process line [%s]" % (ds_filename, line)
        raise
    f = open(ds_filename, "w")
    f.write("\n".join(map(lambda x: str(x), filtered_ds)))
    f.close()
    
#==============================================================================
# Removes Food Wrong Averages and Variances
#==============================================================================     
def removeWrongFoodcomValues(ds_filename):        
    filtered_ds = []
    try:
        with open(ds_filename) as f:
            for line in f:
                st_idx = line.index(SEP_CHAR+"250767:")
                line = line.replace(' ', '\t')
                filtered_ds.append(line[:st_idx])           
        f.close()
    except IOError:
        print "Error opening file %s" % ds_filename
        raise
    except ValueError:
        print "File[%s]ERROR::Could not process line [%s]" % (ds_filename, line)
        raise
    f = open(ds_filename, "w")
    f.write("\n".join(map(lambda x: str(x), filtered_ds)))
    f.close()
    
#==============================================================================
# Trunk the ds_filename dataset to the first 3 columns
#==============================================================================     
def trunckDataSet(ds_filename):        
    filtered_ds = []
    try:
        with open(ds_filename) as f:
            for line in f:
                columns = line.split('\t')
                simple = '\t'.join(columns[:3])
                filtered_ds.append(simple.strip())           
        f.close()
    except IOError:
        print "Error opening file %s" % ds_filename
        raise
    except ValueError:
        print "File[%s]ERROR::Could not process line [%s]" % (ds_filename, line)
        raise
    f = open(ds_filename+".txt", "w")
    f.write("\n".join(map(lambda x: str(x), filtered_ds)))
    f.close()


#==============================================================================
# Removes features on dsmask and creates a new file based on ds_basefn+supersetfn features (wihtout dsmask features)
#==============================================================================     
def removeFeatures(ds_basefn, dsmask_fn, ds_supersetfn):        
    mask_lines = []
    superset_lines = []
    base_lines = []
    try:        
        with open(dsmask_fn) as fmask:
            mask_lines = fmask.readlines()
        fmask.close()
        with open(ds_supersetfn) as fsuperset:
            superset_lines = fsuperset.readlines()
        fsuperset.close()
        with open(ds_basefn) as fbase:
            base_lines = fbase.readlines()
        fbase.close()
        # for each line
        for i, line in enumerate(mask_lines):
            # subtract strings
            remaining = superset_lines[i]
            line = line.strip()
            remaining = remaining.replace(line, "")
            # add subtract result to base
            superset_lines[i] = base_lines[i].strip() + '\t' + remaining.strip()
        #save final file
        f = open(ds_supersetfn + ".txt", "w")
        f.write("\n".join(map(lambda x: str(x), superset_lines)))
        f.close()
        print ds_supersetfn + " result file saved"
    except IOError:
        print "Error opening file"
        raise
    except ValueError:
        print "ERROR::Could not process line"
        raise
    return 1

                
