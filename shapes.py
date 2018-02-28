import pandas as pd
import numpy as np
import re
import math
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep
import datetime
import sys
import signal


#Reading dataset
data = pd.read_csv('Latest_Merged_Dataset_0227.csv', encoding='ISO-8859-1', error_bad_lines=False)

#checking if cell is blank
def is_nan(x):
    return isinstance(x, float) and math.isnan(x)

#getting list of shapes from description
def get_shapes(data1):
	shapes = ['changed', 'changing', 'chevron', 'cigar', 'circle', 'circular','cone','cresent','cross','cylinder','delta','diamond','dome','disk','egg','fireball','flare','flash','hexagon','light','oval','pyramind','rectangle','rectangular','round','sphere','teardrop','triangle','triangular']
	df = pd.DataFrame(data1, columns = ['index1','index2','description','duration','location','reported_at','shape','sighted_at','geocoded_latitude','geocoded_longitude','closest_LARGE_airport_name','closest_LARGE_airport_distance','closest_MEDIUM_airport_name','closest_MEDIUM_airport_distance','closest_SMALL_airport_name','closest_SMALL_airport_distance','closest_CLOSED_airport_name','closest_CLOSED_airport_distance','closest_airport_distance','closest_airport_name','city','state','meteor_name','distance_to_meteor','reason','metorite_lat','metorite_long'])
	
	shape_list = []
	desp = []


	for index, row in df.iterrows():
		desp = row['description'].split()
		
		shape = row['shape']
		if is_nan(shape): 
			
			#set to store shapes from description
			words = set()
			
			for word in desp:
				for word1 in shapes:
					if word == word1:
						if word not in words:
							words.add(word)

			#converting list to string
			words = ",".join(words)
			if not words:
				shape_list.append("NA")
			else:
				shape_list.append(words)	
		else:
			shape_list.append(shape)

	df['shape'] = shape_list	

	#write to same data set
	df.to_csv('Latest_Merged_Dataset_0227.csv', encoding='utf-8')

get_shapes(data)
