# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 17:21:18 2015

@author: rui.maia
"""
import csv
import pandas as pd
import numpy as np

def foodds_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    total_rat_cnt = 0
    complete_ds = []
    print "Datafile:%s" % datafile
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

def foodds2_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ARSU,ARSI,NRU,NARI)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for ARSU
                feature_id = hash_fea.get('ARSU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSU'], ARSU)) # append user feature to libSVM format
                # get id for ARSI
                feature_id = hash_fea.get('ARSI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSI'], ARSI)) # append user feature to libSVM format
                # get id for NRU
                feature_id = hash_fea.get('NRU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NRU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NRU'], NRU)) # append user feature to libSVM format
                # get id for NARI
                feature_id = hash_fea.get('NARI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NARI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NARI'], NARI)) # append user feature to libSVM format

                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

def foodds21_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ARSU,ARSI)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for ARSU
                feature_id = hash_fea.get('ARSU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSU'], ARSU)) # append user feature to libSVM format
                # get id for ARSI
                feature_id = hash_fea.get('ARSI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSI'], ARSI)) # append user feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)
		
def foodds3_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ARSU,ARSI,NRU,NARI,ingredient_str)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                ingredient_list = ingredient_str.split(',')
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for ARSU
                feature_id = hash_fea.get('ARSU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSU'], ARSU)) # append user feature to libSVM format
                # get id for ARSI
                feature_id = hash_fea.get('ARSI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSI'], ARSI)) # append user feature to libSVM format
                # get id for NRU
                feature_id = hash_fea.get('NRU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NRU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NRU'], NRU)) # append user feature to libSVM format
                # get id for NARI
                feature_id = hash_fea.get('NARI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NARI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NARI'], NARI)) # append user feature to libSVM format
                # for each ingredient
                for ing in ingredient_list:
                    # get id for recipeid
                    feature_id = hash_ing.get(ing, 0)
                    # if null, add id and increment unique_identifier
                    if (feature_id == 0):
                        hash_ing[ing] = unique_id
                        unique_id += 1
                    entry.append("%d:1" % hash_ing[ing]) # append ingredient feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

def foodds8_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ingredient_str)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                ingredient_list = ingredient_str.split(',')
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # for each ingredient
                for ing in ingredient_list:
                    # get id for recipeid
                    feature_id = hash_ing.get(ing, 0)
                    # if null, add id and increment unique_identifier
                    if (feature_id == 0):
                        hash_ing[ing] = unique_id
                        unique_id += 1
                    entry.append("%d:1" % hash_ing[ing]) # append ingredient feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

def food_arr_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ARSI)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for ARSI
                feature_id = hash_fea.get('ARSI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSI'], ARSI)) # append user feature to libSVM format

                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)
		

        
def food_aur_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,ARSU)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for ARSU
                feature_id = hash_fea.get('ARSU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['ARSU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['ARSU'], ARSU)) # append user feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)
		
        
def food_crr_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,NARI)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for NARI
                feature_id = hash_fea.get('NARI', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NARI'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NARI'], NARI)) # append user feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

		
        
def food_cur_csvtolibsvm(datafile, outdatafile):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    hash_fea = {}
    total_rat_cnt = 0
    complete_ds = []
    try:
        with open(datafile) as f:
            for line in f:
                entry = []
                line = line.strip()
                (rating,user,recipeid,NRU)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append user feature to libSVM format
                # get id for NRU
                feature_id = hash_fea.get('NRU', 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_fea['NRU'] = unique_id
                    unique_id += 1
                entry.append("%d:%s" % (hash_fea['NRU'], NRU)) # append user feature to libSVM format
                complete_ds.append(entry)        
                total_rat_cnt += 1          
    except ValueError:
        print "Error on line %d" % total_rat_cnt
        raise
    print total_rat_cnt
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)

total_ing_error = 0
total_event_error = 0

def ing_split_clena (ingredient):
    global total_ing_error 
    ing_res = ingredient.strip()
    try:
        ing_res = ing_res.split(":")[1]
    except:
        total_ing_error += 1
    return ing_res


def kochbar_csvtolibsvm(datafile, outdatafile, with_ing):
    unique_id = 1
    hash_user = {}
    hash_rec = {}
    hash_ing = {}
    total_rat_cnt = 0
    complete_ds = []
    with open(datafile) as f:
        next(f)
        global total_ing_error 
        global total_event_error
        total_ing_error = 0
        total_event_error = 0
        for line in f:
            try:
                entry = []
                line = line.strip()
                line=line.replace('"', '')
                (recipeid, user, rating, ingredients)=line.split('\t')
                entry.append(rating)    # append rating to libSVM format
                # get id for user
                feature_id = hash_user.get(user, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_user[user] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_user[user]) # append user feature to libSVM format
                # get id for recipeid
                feature_id = hash_rec.get(recipeid, 0)
                # if null, add id and increment unique_identifier
                if (feature_id == 0):
                    hash_rec[recipeid] = unique_id
                    unique_id += 1
                entry.append("%d:1" % hash_rec[recipeid]) # append recipe feature to libSVM format
                if (with_ing == True):      
                    ing_lst = ingredients.split("\\n")
                    ing_lst = map(lambda x:ing_split_clena(x), ing_lst)
                    for ing in ing_lst:
                        # get id for ingredient
                        ing_id = hash_rec.get(ing, 0)
                        # if null, add id and increment unique_identifier
                        if (ing_id == 0):
                            hash_ing[ing_id] = unique_id
                            unique_id += 1
                        entry.append("%d:1" % hash_ing[ing_id]) # append ingredient feature to libSVM format
                complete_ds.append(entry)                    
                total_rat_cnt += 1          
            except ValueError:
                total_event_error += 1
    print 'Total Rating Count:%d' % total_rat_cnt
    print 'Total Ingredient Line Errors:%d' % total_ing_error
    print 'Total Rating Event Errors:%d' % total_event_error
    with open(outdatafile, 'wb') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(complete_ds)
    with open(outdatafile+'nextfree_id.txt', 'w') as nf:
        nf.write("%d" % unique_id)
    print 'Finished converting from csv to libsvm.\nNext free id:' + str (unique_id)


