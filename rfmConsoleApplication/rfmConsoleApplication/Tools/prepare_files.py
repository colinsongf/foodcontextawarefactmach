# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 14:06:13 2015

@author: rui.maia
"""
import sys
import os
sys.path.append(os.path.abspath("Tools"))
from preprocess import *
from csv_to_libsvm import *

###### Remove all the untrustable users and items (with less than 4 assotiated rating events)
# epicuriousQualityFilter('Data\\epicurious.txt', 'Data\\epicurious_ds', 4, 4)
###### Load recipe data (ingredients, cuisine, dietary,...)
recipe_inf = epicuriousLoadData('Data\\Recipes')
# Generate base datasets 
epicuriousGenerateDS('Data\\epicurious_ds', recipe_inf)

'''
# Remove all the untrustable users and items (with less than 4 assotiated rating events)
epicuriousPreprocess('Data\\epicurious.txt', 'Data\\epicurious_ds', 4, 4)
# Load recipe data (ingredients, cuisine, dietary,...)
recipe_inf = epicuriousLoadData('Data\\Recipes')
# Generate base datasets 
epicuriousGenerateBaseDS('Data\\epicurious_ds.txt', recipe_inf)


# Convert to libsvm format

# generate datasets 
splitKFoldSave('Data\\', 'epicurious_ds', 5, 0, 0, 'epicurious_ds')
splitKFoldSave('Data\\', 'epicurious_ds', 5, AVG_USER, 0, 'epicurious_ds2')
splitKFoldSave('Data\\', 'epicurious_ds', 5, AVG_STD_USER, 0, 'epicurious_ds3')
splitKFoldSave('Data\\', 'epicurious_ds', 5, 0, AVG_ITEM, 'epicurious_ds4')
splitKFoldSave('Data\\', 'epicurious_ds', 5, 0, AVG_STD_ITEM, 'epicurious_ds5')
splitKFoldSave('Data\\', 'epicurious_ds', 5, AVG_USER, AVG_ITEM, 'epicurious_ds6')
splitKFoldSave('Data\\', 'epicurious_ds', 5, AVG_STD_USER, AVG_STD_ITEM, 'epicurious_ds7')
---





foodPreprocess('Data\\foodcom.txt', 'Data\\foodcom_ds', 4, 4)

kochbarPreprocess('Data\\recipes.csv', 'Data\\recipes_ratings.csv', 'Data\\recipes_category.csv', 'Data\\kochbar_ds', 'Data\\kochbar_ds8', 'Data\\kochbar_ds14', 'Data\\kochbar_ds15', 4, 4)





splitKFoldSave('epicurious_ds10', str(sys.argv[2]), 5, AVG_USER, AVG_ITEM, 'epicurious_ds13')
removeWrongEpicuriousValues('Data\epicurious_ds8')
removeWrongEpicuriousValues('Data\epicurious_ds9')
removeWrongEpicuriousValues('Data\epicurious_ds10')
splitKFoldSave('Data\\', 'epicurious_ds8',  5, 0, 0, 'epicurious_ds8')
splitKFoldSave('Data\\', 'epicurious_ds9', 5, 0, 0, 'epicurious_ds9')
splitKFoldSave('Data\\', 'epicurious_ds10', 5, 0, 0, 'epicurious_ds10')
splitKFoldSave('Data\\', 'epicurious_ds8',  5, AVG_USER, AVG_ITEM, 'epicurious_ds11')
splitKFoldSave('Data\\', 'epicurious_ds9', 5, AVG_USER, AVG_ITEM, 'epicurious_ds12')
splitKFoldSave('Data\\', 'epicurious_ds10', 5, AVG_USER, AVG_ITEM, 'epicurious_ds13')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, 0, 0, 'foodcom_ds')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, AVG_USER, 0, 'foodcom_ds2')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, AVG_STD_USER, 0, 'foodcom_ds3')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, 0, AVG_ITEM, 'foodcom_ds4')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, 0, AVG_STD_ITEM, 'foodcom_ds5')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, AVG_USER, AVG_ITEM, 'foodcom_ds6')
splitKFoldSave('Data\\', 'foodcom_ds_svm', 5, AVG_STD_USER, AVG_STD_ITEM, 'foodcom_ds7')
removeWrongFoodcomValues('Data\\foodcom_ds9')
removeWrongFoodcomValues('Data\\foodcom_ds10')
removeWrongFoodcomValues('Data\\foodcom_ds11')
splitKFoldSave('Data\\', 'foodcom_ds8',  5, 0, 0, 'foodcom_ds8')
splitKFoldSave('Data\\', 'foodcom_ds9', 5, 0, 0, 'foodcom_ds9')
splitKFoldSave('Data\\', 'foodcom_ds10', 5, 0, 0, 'foodcom_ds10')
splitKFoldSave('Data\\', 'foodcom_ds8',  5, AVG_USER, AVG_ITEM, 'foodcom_ds11')
splitKFoldSave('Data\\', 'foodcom_ds9', 5, AVG_USER, AVG_ITEM, 'foodcoms_ds12')
splitKFoldSave('Data\\', 'foodcom_ds10', 5, AVG_USER, AVG_ITEM, 'foodcom_ds13')

addUserRatingCount('Data\\epicurious_ds', 5)
addUserRatingCount('Data\\epicurious_ds2', 5)
addUserRatingCount('Data\\epicurious_ds3', 5)
addUserRatingCount('Data\\epicurious_ds4', 5)
addUserRatingCount('Data\\epicurious_ds5', 5)
addUserRatingCount('Data\\epicurious_ds6', 5)
addUserRatingCount('Data\\epicurious_ds7', 5)
addUserRatingCount('Data\\epicurious_ds8', 5)
addUserRatingCount('Data\\epicurious_ds9', 5)
addUserRatingCount('Data\\epicurious_ds10', 5)
addUserRatingCount('Data\\epicurious_ds11', 5)
addUserRatingCount('Data\\epicurious_ds12', 5)
addUserRatingCount('Data\\epicurious_ds13', 5)

addUserRatingCount('Data\\foodcom_ds', 5)
addUserRatingCount('Data\\foodcom_ds2', 5)
addUserRatingCount('Data\\foodcom_ds3', 5)
addUserRatingCount('Data\\foodcom_ds4', 5)
addUserRatingCount('Data\\foodcom_ds5', 5)
addUserRatingCount('Data\\foodcom_ds6', 5)
addUserRatingCount('Data\\foodcom_ds7', 5)

addUserRatingCount('Data\\foodcom_ds8', 5)
addUserRatingCount('Data\\foodcom_ds9', 5)
addUserRatingCount('Data\\foodcom_ds10', 5)
addUserRatingCount('Data\\foodcom_ds11', 5)
addUserRatingCount('Data\\foodcom_ds12', 5)
addUserRatingCount('Data\\foodcom_ds13', 5)

removeEpicuriousFeatures('Data\\epicurious_ds', 'Data\\epicurious_ds8', 'Data\\epicurious_ds9')
removeEpicuriousFeatures('Data\\epicurious_ds', 'Data\\epicurious_ds9', 'Data\\epicurious_ds10')

splitKFoldSave('Data\\', 'epicurious_ds14',  5, 0, 0, 'epicurious_ds14')
splitKFoldSave('Data\\', 'epicurious_ds15',  5, 0, 0, 'epicurious_ds15')
splitKFoldSave('Data\\', 'epicurious_ds14',  5, 1, 1, 'epicurious_ds16')
splitKFoldSave('Data\\', 'epicurious_ds15',  5, 1, 1, 'epicurious_ds17')


removeFeatures('Data\\foodcom_ds', 'Data\\foodcom_ds8', 'Data\\foodcom_ds9')
removeFeatures('Data\\foodcom_ds', 'Data\\foodcom_ds9', 'Data\\foodcom_ds10')

splitKFoldSave('Data\\', 'foodcom_ds14',  5, 0, 0, 'foodcom_ds14')
splitKFoldSave('Data\\', 'foodcom_ds15',  5, 0, 0, 'foodcom_ds15')
splitKFoldSave('Data\\', 'foodcom_ds14',  5, 1, 1, 'foodcom_ds16')
splitKFoldSave('Data\\', 'foodcom_ds15',  5, 1, 1, 'foodcom_ds17')

cutSave('Data\\foodcom_ds', 86575)
cutSave('Data\\foodcom_ds8', 86575)
cutSave('Data\\foodcom_ds9', 86575)
cutSave('Data\\foodcom_ds10', 86575)
cutSave('Data\\foodcom_ds14', 86575)
cutSave('Data\\foodcom_ds15', 86575)
splitKFoldSave('Data\\', 'foodcom_ds', 5, 0, 0, 'foodcom_ds')
splitKFoldSave('Data\\', 'foodcom_ds', 5, AVG_USER, 0, 'foodcom_ds2')
splitKFoldSave('Data\\', 'foodcom_ds', 5, AVG_STD_USER, 0, 'foodcom_ds3')
splitKFoldSave('Data\\', 'foodcom_ds', 5, 0, AVG_ITEM, 'foodcom_ds4')
splitKFoldSave('Data\\', 'foodcom_ds', 5, 0, AVG_STD_ITEM, 'foodcom_ds5')
splitKFoldSave('Data\\', 'foodcom_ds', 5, AVG_USER, AVG_ITEM, 'foodcom_ds6')
splitKFoldSave('Data\\', 'foodcom_ds', 5, AVG_STD_USER, AVG_STD_ITEM, 'foodcom_ds7')
splitKFoldSave('Data\\', 'foodcom_ds8',  5, 0, 0, 'foodcom_ds8')
splitKFoldSave('Data\\', 'foodcom_ds9', 5, 0, 0, 'foodcom_ds9')
splitKFoldSave('Data\\', 'foodcom_ds10', 5, 0, 0, 'foodcom_ds10')
splitKFoldSave('Data\\', 'foodcom_ds8',  5, AVG_USER, AVG_ITEM, 'foodcom_ds11')
splitKFoldSave('Data\\', 'foodcom_ds9', 5, AVG_USER, AVG_ITEM, 'foodcom_ds12')
splitKFoldSave('Data\\', 'foodcom_ds10', 5, AVG_USER, AVG_ITEM, 'foodcom_ds13')
splitKFoldSave('Data\\', 'foodcom_ds14',  5, 0, 0, 'foodcom_ds14')
splitKFoldSave('Data\\', 'foodcom_ds15',  5, 0, 0, 'foodcom_ds15')
splitKFoldSave('Data\\', 'foodcom_ds14',  5, 1, 1, 'foodcom_ds16')
splitKFoldSave('Data\\', 'foodcom_ds15',  5, 1, 1, 'foodcom_ds17')


splitKFoldSave('Data\\', 'kochbar_ds', 5, 0, 0, 'kochbar_ds')
splitKFoldSave('Data\\', 'kochbar_ds', 5, AVG_USER, 0, 'kochbar_ds2')
splitKFoldSave('Data\\', 'kochbar_ds', 5, AVG_STD_USER, 0, 'kochbar_ds3')
splitKFoldSave('Data\\', 'kochbar_ds', 5, 0, AVG_ITEM, 'kochbar_ds4')
splitKFoldSave('Data\\', 'kochbar_ds', 5, 0, AVG_STD_ITEM, 'kochbar_ds5')
splitKFoldSave('Data\\', 'kochbar_ds', 5, AVG_USER, AVG_ITEM, 'kochbar_ds6')
splitKFoldSave('Data\\', 'kochbar_ds', 5, AVG_STD_USER, AVG_STD_ITEM, 'kochbar_ds7')


cutSave('Data\\kochbar86k_ds', 86575)

splitKFoldSave('Data\\', 'kochbar86k_ds', 5, 0, 0, 'kochbar86k_ds')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, AVG_USER, 0, 'kochbar86k_ds2')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, AVG_STD_USER, 0, 'kochbar86k_ds3')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, 0, AVG_ITEM, 'kochbar86k_ds4')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, 0, AVG_STD_ITEM, 'kochbar86k_ds5')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, AVG_USER, AVG_ITEM, 'kochbar86k_ds6')
splitKFoldSave('Data\\', 'kochbar86k_ds', 5, AVG_STD_USER, AVG_STD_ITEM, 'kochbar86k_ds7')


'''

print 'Prepare Files DONE!'
