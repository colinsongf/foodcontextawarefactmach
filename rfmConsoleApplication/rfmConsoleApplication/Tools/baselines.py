# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:21:21 2015

@author: rui.maia
"""

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from math import sqrt

SEP_CHAR = '\t'

def dsAVGandSTD(datafile, saveOutput):
    item_dic = {}
    user_dic = {}
    try:
        print 'Calculating user and item Avg&STD on %s' % datafile
        with open(datafile) as f:
            for i, line in enumerate(f):            
                #add row to result
                rate_evt = line.split(SEP_CHAR)
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
            f.close()
            ################################################
            # Calculate average rating of each user 
            ################################################
            for key, entry in user_dic.items():
                entry['avg'] = np.average(entry['events'])
                entry['std'] = np.std(entry['events'])
            if (saveOutput):
                uf = open(datafile+'.user.avgstd', 'w')
                uf.write('Average\tStdDeviation\n')
                for key, entry in user_dic.items():
                    uf.write('%s\t%s\n' % (entry['avg'], entry['std']))            
            ################################################
            # Calculate average rating of each item
            ################################################           
            for key, entry in item_dic.items():
                entry['avg'] = np.average(entry['events'])
                entry['std'] = np.std(entry['events'])                
            if (saveOutput):
                uf = open(datafile+'.item.avgstd', 'w')
                uf.write('Average\tStdDeviation\n')
                for key, entry in item_dic.items():
                    uf.write('%s\t%s\n' % (entry['avg'], entry['std']))                    
    except ValueError:
        print "Error on line [%s]" % i
        raise 
    except IndexError:
        print "Error on line [%s]" % i
        raise 
    return (user_dic, item_dic)

def dsMAEandRMSE(datafile, nFolds):
    print 'Calculating RMSE for User Average Rating'
    print "Basefilename:%s" % datafile
    print "Number of Folds:%d" % nFolds
    #EXAMPLE
    #epicurious_ds5.1.base.libfm
    #epicurious_ds5.1.test.libfm    
    try:
        rmse_arr = []
        mae_arr = []
        # for each k-fold
        for x in range(1,nFolds+1):
            user_dic, item_dic = dsAVGandSTD(datafile + "." + str(x) + ".base.libfm", False)
            filename = datafile + "." + str(x) + ".test.libfm"
            with open(filename) as tf:
                target_y = []
                estimated_y = []
                # for each line
                for line in tf:
                    # split training line by target and feature
                    rate_evt = line.split(SEP_CHAR)
                    # add target to y_vector
                    target_y.append(float(rate_evt[0]))
                    # add user-avg to estimated_vetor
                    #estimated_y.append(float(rate_evt[3].split(':')[1]))
                    user = user_dic.get(rate_evt[1], 0)
                    if (user == 0):
                        estimated_y.append(float(0))
                    else:
                        estimated_y.append(float(user['avg']))                    
                # get rmse for y_vector and estimated_vector
                rmse_arr.append(sqrt(mean_squared_error(target_y, estimated_y)))
                # get mae for y_vector and estimated_vector
                mae_arr.append(mean_absolute_error(target_y, estimated_y))
                print filename + '[RMSE]:' + str('%.4f' % rmse_arr[-1])
                print filename + '[MAE]:' + str('%.4f' % mae_arr[-1])
        print 'Average (all k-Folds) RSME for Avg Based Prediction using ' + filename + ' is:' + str('%.4f' % np.mean(rmse_arr))
        print 'Average (all k-Folds) MAE for Avg Based Prediction using ' + filename + ' is:' + str('%.4f' % np.mean(mae_arr))
        resfn = datafile + '.rmse.avg'
        resfn = resfn.replace("Data", "Results")
        myfile = open(resfn, 'w')
        myfile.write(str(np.mean(rmse_arr)))
        resfn = datafile + '.mae.avg'
        resfn = resfn.replace("Data", "Results")
        myfile = open(resfn, 'w')
        myfile.write(str(np.mean(mae_arr)))
    except ValueError:
        print "Error"
        raise
    return 1


#dsMAEandRMSE('Data\epicurious_ds', 5)
# Calculate and Save User and Item Standard Deviation and Average Rating
#dsAVGandSTD('Data\epicurious_ds', True)

#dsMAEandRMSE('Data\\foodcom_ds', 5)
# Calculate and Save User and Item Standard Deviation and Average Rating
#dsAVGandSTD('Data\\foodcom_ds', True)

#dsMAEandRMSE('Input\\kochbar_ds', 5)
# Calculate and Save User and Item Standard Deviation and Average Rating
#dsAVGandSTD('Input\\kochbar_ds', True)



print 'Ending calculating the baselines'