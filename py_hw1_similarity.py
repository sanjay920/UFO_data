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
REF_DATA_FILE = "merge_data/ufo_dataset_final_with_lat_lon.csv"
INPUT_DATA_FILE = "merge_data/normalized_dataset_final_with_lat_lon.csv"
EDIT_DIST_CSV_FILE = "edit_distance_similarity.csv"
COSINE_SIMILARITY_CSV_FILE = "cosine_similarity.csv"
JACCARD_SIMILARITY_CSV_FILE="jaccard_similarity.csv"



# ######################## Sampling the input data and normalizing the columns. To be improved and investigated further
data = pd.read_csv(INPUT_DATA_FILE)
ref_data = pd.read_csv(REF_DATA_FILE)
# data = data.loc[data['state'] == 'California']

data = data.sample(50)
data_dictionary = defaultdict()
index_to_state = defaultdict()

# ########################################################################################################

# print data['closest_SMALL_airport_distance']

# Create a dictionary of items - Key: Location of the ufo sighting, value- feature
columns = list(data)
for index,row in data.iterrows():
    # print row
    feature = defaultdict()
    # feature['medium_airport'] = row['medium_airport_category']
    # feature['small_airport'] = row['small_airport_category']
    # feature['large_airport'] = row['large_airport_category']
    # feature['meteorite'] = row['meteor_sighting']
    # feature['metro_distance'] = row['metro_distance_category']
    # feature['closest_metro_m4'] = row['closest_metro_m4']
    # feature['closest_metro_m6'] = row['closest_metro_m6']
    for feat_name in columns:
        if feat_name != "id":
            feature[feat_name] = row[feat_name]
    # feature['population'] = row['population']
    # location = row['location'].split(',')[0]
    data_dictionary[row['id']] = feature
    ref_row = ref_data[ref_data['id'] == row['id']]
    # print ref_row.iloc[0]['state']
    # break
    index_to_state[row['id']] = str(row['id']) + "S" + ref_row.iloc[0]['state']

tuples = itertools.combinations(data_dictionary.keys(),2)


def compute_cosine_similarity(tuples):
    with open(COSINE_SIMILARITY_CSV_FILE, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        for sighting_1, sighting_2 in tuples:
            try:
                raw_cosine_distance = [index_to_state[sighting_1], index_to_state[sighting_2]]
                v1 = Vector(sighting_1, data_dictionary[sighting_1])
                v2 = Vector(sighting_2, data_dictionary[sighting_2])
                raw_cosine_distance.append(round(v1.cosTheta(v2),2))
                a.writerow(raw_cosine_distance)
            except:
                continue

def compute_edit_distance(tuples):
    with open(EDIT_DIST_CSV_FILE, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        for sighting_1, sighting_2 in tuples:
            try:
                raw_edit_distance = [sighting_1, sighting_2]
                v1 = Vector(sighting_1, data_dictionary[sighting_1])
                v2 = Vector(sighting_2, data_dictionary[sighting_2])
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



def jaccard_similarity(tuples):
    with open(JACCARD_SIMILARITY_CSV_FILE,"wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        # row = []
        for sighting_1, sighting_2 in tuples:
            try:
                result = jaccard(data_dictionary[sighting_1], data_dictionary[sighting_2])
                row = (sighting_1, sighting_2, result)
                a.writerow(row)
            except:
                continue


compute_cosine_similarity(tuples)
