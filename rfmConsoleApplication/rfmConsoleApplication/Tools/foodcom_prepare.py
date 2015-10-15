# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:39:31 2015

This file provides the routines to preprocess and prepare foodcom data in order
to have a quality set of datasets, following some simple rules:
- users have at least 4 event ratings
- items/recipes have at least 4 event ratings
- the output files will be in libsvm format

@author: rui.maia
"""
from __future__ import division
import sys
import os
sys.path.append(os.path.abspath("Tools"))
from preprocess import *
import pandas as pd
import csv
from random import shuffle


AVG_USER = 1
STD_USER = 2
AVG_STD_USER = 3
AVG_ITEM = 1
STD_ITEM = 2
AVG_STD_ITEM = 3

next_free_id = 1
hash_user = {}
hash_rec = {}
hash_ing = {}
hash_diet = {}
hash_cuis = {}

#==============================================================================
# Receives a dataset and ovewrites it cutting the original file to a 
# count (input parameter) number of entries
#==============================================================================
def foodcom_CutSave(datafile, count):
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
    

########################################################################################
# Remove foodcom untrustable ratings (count item and user rating events, then filter)
########################################################################################
def foodcom_QualityFilter(rat_ds, out_base_ds, min_user, min_item):
    # pass in column names for each CSV
    print 'Loading ratings...'    
    ratings_cols = ['rating', 'user', 'id']
    ratings = pd.read_csv(rat_ds, sep='\t', names=ratings_cols)
    print 'Ratings Shape: %s' % str(ratings.shape)
    print 'Remove untrustable users and recipes...'
    atleast_5 = ratings.groupby('id').filter(lambda x: len(x) >= min_item)
    print 'Ratings (>' + str(min_item) +  ' item event rating) shape' + str(atleast_5.shape)
    final_ds = atleast_5.groupby('user').filter(lambda y: len(y) >= min_user)
    print 'Ratings (>' + str(min_user) + ' user event rating) shape' + str(final_ds.shape)
    ######################### DS OUPUT
    final_ds_len = final_ds.shape[0]
    atleast_5_len = atleast_5.shape[0]
    while final_ds_len != atleast_5_len:
        print 'Remove untrustable users and recipes...'
        atleast_5 = final_ds.groupby('id').filter(lambda x: len(x) >= min_item)
        print 'Ratings (>' + str(min_item) + ' item event rating) shape' + str(atleast_5.shape)
        final_ds = atleast_5.groupby('user').filter(lambda y: len(y) >= min_user)
        print 'Ratings (> ' + str(min_user) + ' user event rating) shape' + str(final_ds.shape)
        final_ds_len = final_ds.shape[0]
        atleast_5_len = atleast_5.shape[0]    
    print 'Saving DS base dataset with shape ' + str(final_ds.shape)
    final_ds.to_csv(out_base_ds, sep='\t', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id'])    
    print '...done'     



###########################################################################
######### Load recipe information from files got from foodcom site
###########################################################################
def foodcom_LoadData(rec_ing_file, rec_cuis_file, rec_diet_file):
    data = {}    
    ingredients = {}
    cuisines = {}
    diets = {}
    try:
        # ingredients
        file = open(rec_ing_file)
        for line in file:
            # get recipe id
            fields=line.split('\t')
            rec_id = fields[2].strip()
            # if dictionary empty: set ingredients for recipe                
            if rec_id not in data:
                # get recipe ingredients
                rec_ings = fields[3:]
                for elem in rec_ings: 
                    elem = elem.strip()
                    if len(elem) > 0: ingredients[elem] = ingredients.get(elem, 0) + 1
                tempData = dict()
                tempData['MainIng']=(",".join(rec_ings)).strip()
                data[rec_id] = tempData
    except IndexError:
        print 'Error in file:' + rec_ing_file
        print line
        raise
    try:
        # cuisine
        file = open(rec_cuis_file)
        for line in file:
            # get recipe id
            fields=line.split('\t')
            rec_id = fields[2]
            tempData = data[rec_id.strip()]
            if 'Cuisine' not in tempData:
                # get recipe cuisines
                rec_cuis = fields[3:]
                for elem in rec_cuis: 
                    elem = elem.strip()
                    if len(elem) > 0: cuisines[elem] = cuisines.get(elem, 0) + 1
                tempData['Cuisine']=(",".join(rec_cuis)).strip()
    except IndexError:
        print 'Error in file:' + rec_cuis_file
        print line
        raise
    try:
        # dietary
        file = open(rec_diet_file)
        for line in file:
            # get recipe id
            fields=line.split('\t')
            rec_id = fields[2]
            tempData = data[rec_id.strip()]
            if 'Dietary' not in tempData:
                # get recipe dietaries
                rec_diets = fields[3:]
                for elem in rec_diets: 
                    elem = elem.strip()
                    if len(elem) > 0: diets[elem] = diets.get(elem, 0) + 1
                tempData['Dietary']=(",".join(rec_diets)).strip()                
    except IndexError:
        print 'Error in file:' + rec_diet_file
        print line
        raise
    print 'Recipes (count): %d' % len(data.keys())
    print 'Saving different Ingredients %d' % len(ingredients)
    with open('Data\\foodcom_ingredients.txt', 'w') as writer:
        writer.write('Ingredient\tRecipeCount\n')
        for key, entry in ingredients.items():
            writer.write('%s\t%d\n' % (key.strip(), entry))
    print 'Saving different Cuisines %d' % len(cuisines)
    with open('Data\\foodcom_cuisines.txt', 'w') as writer:
        writer.write('Cuisine\tRecipeCount\n')
        for key, entry in cuisines.items():
            writer.write('%s\t%d\n' % (key.strip(), entry))    
    print 'Saving different Diets %d' % len(diets)
    with open('Data\\foodcom_diets.txt', 'w') as writer:
        writer.write('Diet\tRecipeCount\n')
        for key, entry in diets.items():
            writer.write('%s\t%d\n' % (key.strip(), entry))       
    '''
    for key, value in data.iteritems():  
        if len(value['MainIng']) > 0:
            value['MainIng'] = value['MainIng'][:-1]   
        if len(value['Dietary']) > 0:
            value['Dietary'] = value['Dietary'][:-1]
        if len(value['Cuisine']) > 0:
            value['Cuisine'] = value['Cuisine'][:-1]
    '''
    return data

## Generates the base needed datasets
# pre_foodcom_ds8	- Rating + Users + Item + Ingredients
# pre_foodcom_ds9	- Rating + Users + Item + Ingredients + Dietary
# pre_foodcom_ds10	- Rating + Users + Item + Ingredients + Dietary + Cuisine
# pre_foodcom_ds14 - Rating + Users + Item + Dietary
# pre_foodcom_ds15 - Rating + Users + Item + Cuisine
def foodcom_GenerateBaseDS(basic_ds_path, recipe_inf_lst, out_baseds):
    col_names = ['rating', 'user', 'id', 'ingredients', 'cuisine', 'dietary']
    final = []
    errors = 0    
    with open(basic_ds_path) as basic_ds:
        for line in basic_ds:
            try:        
                (rating, user, item) = (line.strip()).split(SEP_CHAR)
                rec_info = recipe_inf_lst[item]
                final.append((rating, user, item, rec_info['MainIng'], rec_info['Cuisine'], rec_info['Dietary']))
            except KeyError:
                # print line
                #raise
                errors += 1
    print 'Total recipes with info[%d] and no info on [%d]' % (len(final), errors)
    print 'Saving to csv...' 
    complete_ds = pd.DataFrame(final, columns=col_names)
    complete_ds.to_csv(out_baseds, sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'ingredients', 'dietary', 'cuisine'])    
    complete_ds.to_csv('Data\\pre_foodcom_ds', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id'])      
    complete_ds.to_csv('Data\\pre_foodcom_ds8', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'ingredients'])      
    complete_ds.to_csv('Data\\pre_foodcom_ds9', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'ingredients', 'dietary'])    
    complete_ds.to_csv('Data\\pre_foodcom_ds10', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'ingredients', 'dietary', 'cuisine'])    
    complete_ds.to_csv('Data\\pre_foodcom_ds14', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'dietary'])    
    complete_ds.to_csv('Data\\pre_foodcom_ds15', sep=';', encoding='utf-8', index=False, header=False, columns=['rating', 'user', 'id', 'cuisine'])    


def foodcom_GenerateFeatureIds(complete_ds):  
    global next_free_id
    global hash_user
    global hash_rec
    global hash_ing
    global hash_diet
    global hash_cuis
    total_rat_cnt = 0
    total_cui_set = 0
    total_diet_set = 0
    total_ing_set = 0
    rate_sum = 0
    try:
         with open(complete_ds) as f:
            for line in f:
                line = line.strip()
                (rating, user, recipeid, ingredient_str, dietary_str, cuisine_str)=line.split(';')
                rate_sum += int(rating)
                # USER ----------- get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment next_free_identifier
                if (feature_id == 0):
                    hash_user[user] = next_free_id
                    next_free_id += 1
                # RECIPE ---------- get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment next_free_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = next_free_id
                    next_free_id += 1
                # INGREDIENTS -----------------
                if len(ingredient_str) >0:
                    ingredient_list = ingredient_str.split(',')                
                else:
                    ingredient_list = []
                # for each ingredient
                for ing in ingredient_list:
                    total_ing_set += 1
                    # get id for recipeid
                    feature_id = hash_ing.get(ing, 0)
                    # if null, add id and increment next_free_identifier
                    if (feature_id == 0):
                        hash_ing[ing] = next_free_id
                        next_free_id += 1
                # DIETARY -----------------------------
                if len(dietary_str) >0:
                    diet_list = dietary_str.split(',')                
                else:
                    diet_list = []
                # for each ingredient
                for diet in diet_list:
                    total_diet_set += 1
                    # get id for recipeid
                    feature_id = hash_diet.get(diet, 0)
                    # if null, add id and increment next_free_identifier
                    if (feature_id == 0):
                        hash_diet[diet] = next_free_id
                        next_free_id += 1
                # CUISINE  -----------------------------
                if len(cuisine_str) >0:
                    cuis_list = cuisine_str.split(',')                
                else:
                    cuis_list = []
                # for each ingredient
                for cuis in cuis_list:
                    total_cui_set += 1
                    # get id for recipeid
                    feature_id = hash_cuis.get(cuis, 0)
                    # if null, add id and increment next_free_identifier
                    if (feature_id == 0):
                        hash_cuis[cuis] = next_free_id
                        next_free_id += 1
                total_rat_cnt += 1     
    except ValueError:
        print "Error on line %d: %s" % (total_rat_cnt, line)
        raise
    f = open('Data\\foodcom_classification', 'w')
    f.write('Number of users:%d\n' % len(hash_user.keys()))
    f.write('Number of items:%d\n' % len(hash_rec.keys()))
    f.write('Number of events:%d\n' % total_rat_cnt)
    f.write('Number of ingredients:%d\n' % len(hash_ing.keys()))
    f.write('Number of cuisine types:%d\n' % len(hash_cuis.keys()))
    f.write('Number of dietary groups:%d\n' % len(hash_diet.keys()))
    f.write('Avg. rating value:%0.2f\n' % (rate_sum/total_rat_cnt))    
    f.write('Avg. number of ratings per user:%0.2f\n' % (total_rat_cnt/len(hash_user.keys())))
    f.write('Avg. number of ratings per item:%0.2f\n' % (total_rat_cnt/len(hash_rec.keys())))
    f.write('Avg. number of ingredients per item:%0.2f\n' % ((total_ing_set/len(hash_rec.keys()))))
    f.write('Avg. number of cuisine type per item:%0.2f\n' % ((total_cui_set/len(hash_rec.keys()))))
    f.write('Avg. number of dietary groups per item:%0.2f\n' % ((total_diet_set/len(hash_rec.keys()))))
    f.write('Sparsity on the ratings matrix:%0.3f%%\n' % percentage(total_rat_cnt ,(len(hash_user.keys())*len(hash_rec.keys()))))    
    f.close()   
    return next_free_id
    
def percentage(part, whole):
  return 100 * float(part)/float(whole)


def foodcom_CsvtoLibsvm(datafile, outdatafile, is_ing, is_diet, is_cuis):
    global next_free_id
    global hash_user
    global hash_rec
    global hash_ing
    global hash_diet
    global hash_cuis    
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                if (is_ing == False and is_diet == False and is_cuis == False):
                    (rating, user, recipeid)=line.split(';')
                if (is_ing == True and is_diet == False and is_cuis == False):
                    (rating, user, recipeid, ingredient_str)=line.split(';')
                elif (is_ing == True and is_diet == True and is_cuis == False):
                    (rating, user, recipeid, ingredient_str, dietary_str)=line.split(';')
                elif (is_ing == True and is_diet == True and is_cuis == True):
                    (rating, user, recipeid, ingredient_str, dietary_str, cuisine_str)=line.split(';')
                elif (is_ing == False and is_diet == True and is_cuis == False):
                    (rating, user, recipeid, dietary_str)=line.split(';')
                elif (is_ing == False and is_diet == False and is_cuis == True):
                    (rating, user, recipeid, cuisine_str)=line.split(';')
                entry.append(rating)    # append rating to libSVM format
                # USER ----------- get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment next_free_identifier
                if (feature_id == 0):
                    hash_user[user] = next_free_id
                    next_free_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # RECIPE ---------- get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment next_free_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = next_free_id
                    next_free_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # INGREDIENTS -----------------
                if is_ing:
                    if len(ingredient_str) >0:
                        ingredient_list = ingredient_str.split(',')                
                    else:
                        ingredient_list = []
                    # for each ingredient
                    for ing in ingredient_list:
                        # get id for recipeid
                        feature_id = hash_ing.get(ing, 0)
                        # if null, add id and increment next_free_identifier
                        if (feature_id == 0):
                            hash_ing[ing] = next_free_id
                            next_free_id += 1
                        entry.append("%d:1" % hash_ing[ing]) # append ingredient feature to libSVM format
                # DIETARY -----------------------------
                if is_diet:
                    if len(dietary_str) >0:
                        diet_list = dietary_str.split(',')                
                    else:
                        diet_list = []
                    # for each ingredient
                    for diet in diet_list:
                        # get id for recipeid
                        feature_id = hash_diet.get(diet, 0)
                        # if null, add id and increment next_free_identifier
                        if (feature_id == 0):
                            hash_diet[diet] = next_free_id
                            next_free_id += 1
                        entry.append("%d:1" % hash_diet[diet]) # append dietary feature to libSVM format
                # CUISINE  -----------------------------
                if is_cuis:
                    if len(cuisine_str) >0:
                        cuis_list = cuisine_str.split(',')                
                    else:
                        cuis_list = []
                    # for each ingredient
                    for cuis in cuis_list:
                        # get id for recipeid
                        feature_id = hash_cuis.get(cuis, 0)
                        # if null, add id and increment next_free_identifier
                        if (feature_id == 0):
                            hash_cuis[cuis] = next_free_id
                            next_free_id += 1
                        entry.append("%d:1" % hash_cuis[cuis]) # append cuisine feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d: %s" % (total_rat_cnt, line)
        raise
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)
    print 'Saved file %s with %d entries' % (outdatafile, total_rat_cnt)
    return next_free_id
   

def foodcom_GenerateStatsDS():
    global next_free_id
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds', 'Data\\foodcom_ds', False, False, False)
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, 0, 0, 'foodcom_ds')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, AVG_USER, 0, 'foodcom_ds2')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, AVG_STD_USER, 0, 'foodcom_ds3')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, 0, AVG_ITEM, 'foodcom_ds4')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, 0, AVG_STD_ITEM, 'foodcom_ds5')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, AVG_USER, AVG_ITEM, 'foodcom_ds6')
    splitKFoldSave('Data\\', 'foodcom_ds', next_free_id, 5, AVG_STD_USER, AVG_STD_ITEM, 'foodcom_ds7')
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds8', 'Data\\foodcom_ds8', True, False, False)
    splitKFoldSave('Data\\', 'foodcom_ds8', next_free_id,  5, 0, 0, 'foodcom_ds8')
    splitKFoldSave('Data\\', 'foodcom_ds8', next_free_id,  5, AVG_USER, AVG_ITEM, 'foodcom_ds11')    
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds9', 'Data\\foodcom_ds9', True, True, False)
    splitKFoldSave('Data\\', 'foodcom_ds9', next_free_id, 5, 0, 0, 'foodcom_ds9')
    splitKFoldSave('Data\\', 'foodcom_ds9', next_free_id, 5, AVG_USER, AVG_ITEM, 'foodcom_ds12')
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds10', 'Data\\foodcom_ds10', True, True, True)
    splitKFoldSave('Data\\', 'foodcom_ds10', next_free_id, 5, 0, 0, 'foodcom_ds10')      
    splitKFoldSave('Data\\', 'foodcom_ds10', next_free_id, 5, AVG_USER, AVG_ITEM, 'foodcom_ds13')
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds14', 'Data\\foodcom_ds14', False, True, False)
    splitKFoldSave('Data\\', 'foodcom_ds14', next_free_id, 5, 0, 0, 'foodcom_ds14')    
    splitKFoldSave('Data\\', 'foodcom_ds14', next_free_id,  5, 1, 1, 'foodcom_ds16')
    foodcom_CsvtoLibsvm('Data\\pre_foodcom_ds15', 'Data\\foodcom_ds15', False, False, True)
    splitKFoldSave('Data\\', 'foodcom_ds15', next_free_id, 5, 0, 0, 'foodcom_ds15')
    splitKFoldSave('Data\\', 'foodcom_ds15', next_free_id, 5, 1, 1, 'foodcom_ds17')


#foodcom_CutSave('Data\\foodcom.txt', 231355)    
print 'Remove all the untrustable users and items (with less than 4 assotiated rating events)'
foodcom_QualityFilter('Data\\foodcom.txt', 'Data\\pre_foodcom_ds', 4, 4)
'''
print 'Generate base datasets'
foodcom_GenerateBaseDS('Data\\pre_foodcom_ds', foodcom_LoadData('Data\\foodcom_ds8', 'Data\\foodcom_ds14', 'Data\\foodcom_ds15'), 'Data\\foodcom_ds_complete')
print 'Generate feature ids'
foodcom_GenerateFeatureIds('Data\\foodcom_ds_complete')
print 'Next free id:' + str(next_free_id)
print 'Generate statistics datasets (with average and standard deviation'
foodcom_GenerateStatsDS()
'''