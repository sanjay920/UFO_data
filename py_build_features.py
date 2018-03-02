# NOTE : This file is used to featurize our data set based on thresholds.
# Will need to write more on this

import pandas as pd
from collections import defaultdict

# Four categories defined, can add more
MISSING = 0
SMALL = 1
MEDIUM = 2
LARGE = 3

NA = "NA"
BLANK = ""

# Input file goes here
DATA_SET_PATH = 'ufo_dataset_final.csv'
OUTPUT_DATA_FRAME_NAME = 'featurized_data_set.csv'

# TODO: Need to add encoding when reading the data frame
data = pd.read_csv(DATA_SET_PATH)
# data = data.sample(10)

# Tresholds for each feature added so far
SMALL_AD_TRESHOLD = [[0,50], [50,100], [100]]
MEDIUM_AD_TRESHOLD = [[0,50], [50,100], [100]]
LARGE_AD_TRESHOLD = [[0,50], [50,100], [100]]
METRO_DISTANCE_TRESHOLD = [[0,50], [50,100], [100]]
POPULATION_TRESHHOLD = [[0,200000], [200000, 600000], [600000]]

small_airport_dist_category = []
medium_airport_dist_category = []
large_airport_dist_category = []
metro_distance_category = []
population_category = []

# utility function which takes the reference and gives the category
def get_treshold_value(reference_tresh, val):
    if val == NA:
        return MISSING
    elif val >= reference_tresh[0][0] and val <= reference_tresh[0][1]:
        return SMALL
    elif val >= reference_tresh[1][0] and val <= reference_tresh[1][1]:
        return MEDIUM
    else:
        return LARGE


for index, row in data.iterrows():
    small_ad = row['closest_SMALL_airport_distance']
    medium_ad = row['closest_MEDIUM_airport_distance']
    large_ad = row['closest_LARGE_airport_distance']
    metro_distance = row['closest_metro_distance']
    population_cat = row['population']

    small_airport_dist_category.append(get_treshold_value(SMALL_AD_TRESHOLD, small_ad))
    medium_airport_dist_category.append(get_treshold_value(MEDIUM_AD_TRESHOLD, medium_ad))
    large_airport_dist_category.append(get_treshold_value(LARGE_AD_TRESHOLD, large_ad))
    metro_distance_category.append(get_treshold_value(METRO_DISTANCE_TRESHOLD, metro_distance))
    population_category.append(get_treshold_value(POPULATION_TRESHHOLD, population_cat))


# Just making sure that all have the same shape
print len(large_airport_dist_category)
print len(medium_airport_dist_category)
print len(small_airport_dist_category)
print len(metro_distance_category)
print len(population_category)

data['large_airport_category'] = large_airport_dist_category
data['medium_airport_category'] = medium_airport_dist_category
data['small_airport_category'] = small_airport_dist_category
data['metro_distance_category'] = metro_distance_category
data['population_category'] = population_category

# TODO: Add encoding before exporting as csv
data.to_csv(OUTPUT_DATA_FRAME_NAME, index=False)
