# Exploring cosine similarity, jaccard similarity and edit-distance similarity in this file

import tika
from tika import parser
import pandas as pd
import csv
import itertools
from collections import defaultdict
import numpy as np
import math

# Vector class taken from tika-similarity and modified to fit our need
# pass the ufo-sighting name as the key and a list of features as input(min_distance, closest airport and so on)
# Refer to tika similarity for more details on the implementation
class Vector:
    def __init__(self, feat_name, features):
        self.features = features
        self.feat_name = feat_name

    def dotProduct(self, vector2):
        dot_product = 0.0
        intersect_features = set(self.features) & set(vector2.features)

        for feature in intersect_features:
            dot_product += self.features[feature] * vector2.features[feature]
        return dot_product

    def getMagnitude(self):
        totalMagnitude = 0.0
        for key in self.features:
            totalMagnitude += self.features[key] ** 2
        return math.sqrt(totalMagnitude)

    def cosTheta(self, v2):
        '''
        cosTheta = (V1.V2) / (|V1| |V2|)
        cos 0 = 1 implies identical documents
        '''
        return self.dotProduct(v2) / (self.getMagnitude() * v2.getMagnitude())


# Input / Output Files go here
INPUT_DATA_FILE = "df_nearest_airports.csv"
OUTPUT_CSV_FILE = "cosine_sim_airport.csv"



# ######################## Sampling the input data and normalizing the columns. To be improved and investigated further
data = pd.read_csv(INPUT_DATA_FILE, encoding='ISO-8859-1')
data = data.sample(15)
data_dictionary = defaultdict()

max_medium_ad = max(data['closest_MEDIUM_airport_distance'].tolist())
max_small_ad = max(data['closest_SMALL_airport_distance'].tolist())
max_large_ad = max(data['closest_LARGE_airport_distance'].tolist())

min_medium_ad = min(data['closest_MEDIUM_airport_distance'].tolist())
min_small_ad = min(data['closest_SMALL_airport_distance'].tolist())
min_large_ad = min(data['closest_LARGE_airport_distance'].tolist())


data['closest_MEDIUM_airport_distance'] = abs(data['closest_MEDIUM_airport_distance'] - max_medium_ad )/(max_medium_ad-min_medium_ad)
data['closest_SMALL_airport_distance'] = abs(data['closest_SMALL_airport_distance'] - max_small_ad)/(max_small_ad-min_small_ad)
data['closest_LARGE_airport_distance'] = abs(data['closest_LARGE_airport_distance']-max_large_ad)/(max_large_ad-min_large_ad)

data['closest_SMALL_airport_distance'] = [round(x,2) for x in data['closest_SMALL_airport_distance']]
data['closest_MEDIUM_airport_distance'] = [round(x,2) for x in data['closest_MEDIUM_airport_distance']]
data['closest_LARGE_airport_distance'] = [round(x,2) for x in data['closest_LARGE_airport_distance']]
# ########################################################################################################


# Create a dictionary of items - Key: Location of the ufo sighting, value- feature
for index,row in data.iterrows():
    # print row
    feature = defaultdict()
    feature['medium_distance'] = row['closest_MEDIUM_airport_distance']
    feature['small_airport'] = row['closest_SMALL_airport_distance']
    feature['large_airport'] = row['closest_LARGE_airport_distance']
    data_dictionary[row['location']] = feature


# create tuples for ufo sighting and compute their cosine similarity and write them to a file.
with open(OUTPUT_CSV_FILE, "wb") as outF:
    a = csv.writer(outF, delimiter=',')
    a.writerow(["x-coordinate","y-coordinate","Similarity_score"])

    tuples = itertools.combinations(data_dictionary.keys(),2)
    #
    for sighting_1, sighting_2 in tuples:
        try:
            row_cosine_distance = [sighting_1, sighting_2]
            v1 = Vector(sighting_1, data_dictionary[sighting_1])
            v2 = Vector(sighting_2, data_dictionary[sighting_2])
            row_cosine_distance.append(v1.cosTheta(v2))
            a.writerow(row_cosine_distance)
        except:
            continue


# loc_tuple = [{"location":"Iowa City, IA", "dist":0.924687762}, {"location":"Milwaukee, WI", "dist":2.779821499}]
# v1 = Vector(loc_tuple[0]['location'], {"dist":0.924687762, "dist2":10.006})
# v2 = Vector(loc_tuple[1]['location'], {"dist":80.779821499, "dist2":1000000.998886})
#
# print v1.cosTheta(v2)
