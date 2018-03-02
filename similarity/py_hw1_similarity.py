# Exploring cosine similarity, jaccard similarity and edit-distance similarity in this file

import tika
from tika import parser
import pandas as pd
import csv
import itertools
from collections import defaultdict
import numpy as np
import math
import editdistance

# Vector class taken from tika-similarity and modified to fit our need
# pass the ufo-sighting name as the key and a list of features as input(min_distance, closest airport and so on)
# Refer to tika similarity for more details on the implementation
class Vector:
    def __init__(self, feat_name, features):
        self.features = features
        self.feat_name = feat_name

    # Added this function to generate a string from the feature vector
    def stringify(self,feature):
        attribute_value = feature.values()
        # print attribute_value
        attribute_value = [str(x) for x in attribute_value]
        if isinstance(attribute_value, list):
            return str((", ".join(attribute_value)).encode('utf-8').strip())
        else:
            return str(attribute_value.encode('utf-8').strip())

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

    def editDistance(self, v2):
        v1_feature_string = self.stringify(self.features)
        v2_feature_string = self.stringify(v2.features)

        return float(editdistance.eval(v1_feature_string, v2_feature_string))


# Input / Output Files go here
CATEGORIZED_DATA_FILE = "../featurized_data_set.csv"
NORMALIZED_INPUT_DATA_FILE = "../merge_data/normalized_dataset_final_with_lat_lon.csv"


EDIT_DIST_CSV_FILE = "edit_distance_similarity.csv"
COSINE_SIMILARITY_CSV_FILE = "cosine_similarity.csv"
JACCARD_SIMILARITY_CSV_FILE="jaccard_similarity.csv"


CATEGORIZED_FEATURES = ['medium_airport_category', 'small_airport_category', 'large_airport_category', 'meteor_sighting','metro_distance_category', 'closest_metro_m4', 'closest_metro_m6', 'population_category']


# ######################## Sampling the input data and normalizing the columns. To be improved and investigated further
normalized_data = pd.read_csv(NORMALIZED_INPUT_DATA_FILE)
categorized_data = pd.read_csv(CATEGORIZED_DATA_FILE)


# Sampling data
normalized_data = normalized_data.sample(10)
categorized_data = categorized_data.sample(10)

normalized_data_dictionary = defaultdict()
categorized_feat_dictionary = defaultdict()
index_to_state = defaultdict()

# ########################################################################################################

# print data['closest_SMALL_airport_distance']
# Creating categorized feature dictionary
for index, row in categorized_data.iterrows():
    cat_feature = defaultdict()
    for feat_name in CATEGORIZED_FEATURES:
        cat_feature[feat_name] = row[feat_name]

    categorized_feat_dictionary[row['id']] = cat_feature


# Create a dictionary of items - Key: Location of the ufo sighting, value- feature
# Creating a normalized feature dictionary
columns = list(normalized_data)
for index,row in normalized_data.iterrows():
    feature = defaultdict()
    for feat_name in columns:
        if feat_name != "id":
            feature[feat_name] = row[feat_name]
    normalized_data_dictionary[row['id']] = feature
    # ref_row = ref_data[ref_data['id'] == row['id']]
    # print ref_row.iloc[0]['state']
    # break
    # index_to_state[row['id']] = str(row['id']) + "S" + ref_row.iloc[0]['state']

# tuples = itertools.combinations(data_dictionary.keys(),2)


def compute_cosine_similarity(dictionary):
    tuples = itertools.combinations(dictionary.keys(),2)
    with open(COSINE_SIMILARITY_CSV_FILE, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        for sighting_1, sighting_2 in tuples:
            try:
                raw_cosine_distance = [sighting_1, sighting_2]
                v1 = Vector(sighting_1, dictionary[sighting_1])
                v2 = Vector(sighting_2, dictionary[sighting_2])
                raw_cosine_distance.append(round(v1.cosTheta(v2),2))
                a.writerow(raw_cosine_distance)
            except:
                continue

def compute_edit_distance(dictionary):
    tuples = itertools.combinations(dictionary.keys(),2)
    with open(EDIT_DIST_CSV_FILE, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        for sighting_1, sighting_2 in tuples:
            try:
                raw_edit_distance = [sighting_1, sighting_2]
                v1 = Vector(sighting_1, dictionary[sighting_1])
                v2 = Vector(sighting_2, dictionary[sighting_2])
                raw_edit_distance.append(round(v1.editDistance(v2),2))
                a.writerow(raw_edit_distance)
            except:
                continue


def jaccard(v1,v2):
    isCoExistant = lambda k: (k in v2) and (v1[k] == v2[k])
    intersection = reduce(lambda m, k: (m + 1) if isCoExistant(k) else m, v1.keys(), 0)
    union = len(v1.keys()) + len(v2.keys()) - intersection
    jaccard = float(intersection) / union
    return jaccard



def jaccard_similarity(dictionary):
    tuples = itertools.combinations(dictionary.keys(),2)
    with open(JACCARD_SIMILARITY_CSV_FILE,"wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        # row = []
        for sighting_1, sighting_2 in tuples:
            try:
                result = jaccard(dictionary[sighting_1], dictionary[sighting_2])
                row = (sighting_1, sighting_2, result)
                a.writerow(row)
            except:
                continue



# Pass normalized dictionary to compute cosine similarity
compute_cosine_similarity(normalized_data_dictionary)
# Pass categorized dictionary to compute edit-distance and jaccard similarity
compute_edit_distance(categorized_feat_dictionary)
jaccard_similarity(categorized_feat_dictionary)
