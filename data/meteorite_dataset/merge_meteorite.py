# NOTE: Brief overview of the file and process
# Assumptions : As we just have the year and nothing more. Merging the ufo data and metorite data only on the year.
# 1 - For each entry in the ufo data set, get the state and the sighted at year.
# 2 - Filter the metorite data set by year first and then by state. There by limitiing the number of comparisions
# 4 - Compute the distance from the metorite landing and record the observations
# 5 - Append all the findings to the data frame and save it as a dataframe

import pandas as pd
from geopy.distance import vincenty
import json
from datetime import datetime
import math

ufo_sighting = pd.read_csv('../reference_w_loc.csv')
metorite_data = pd.read_csv('us_metorite_landings_with_states.csv')
state_codes = {}

print ufo_sighting.shape

with open('../utility_data/us_states_isocode.txt') as file:
	state_codes = json.load(file)

# Code to add new features

def get_distance_bw_coord(loc1, loc2):
    try:
        dist = vincenty(loc1, loc2).miles
        return dist
    except:
        return float('inf')

# ufo_sighting = ufo_sighting.sample(100)
metorite_years = list(set([int(x) if not math.isnan(x) else 0 for x in metorite_data['year']]))
# metorite_years = set([int(x) for x in metorite_data['year']])
distance_to_meteor = []
meteor_name = []
reason = []
metorite_lat = []
metorite_long = []

# print metorite_years

for index, row in ufo_sighting.iterrows():
	# Cases where sighted_at is invalid
	try:
		sighted_at_year = datetime.strptime(str(row['sighted_at']), "%Y%m%d")
	except:
		# Keeping record of the error type
		distance_to_meteor.append("NA")
		meteor_name.append("NA")
		reason.append("Invalid time format")
		metorite_lat.append("NA")
		metorite_long.append("NA")
		continue
	sighted_at_year = datetime.strptime(str(row['sighted_at']), "%Y%m%d")
	state_name = row['state']
	sighted_at_year = sighted_at_year.year
	ufo_coord = (row['geocoded_latitude'], row['geocoded_longitude'])

	if int(sighted_at_year) in metorite_years:
		df_meteor_by_year = metorite_data.loc[metorite_data['year'] == sighted_at_year]

		min_dist = float('inf')
		metorite_states = list(set(df_meteor_by_year['state']))
		met_name = "NA"
		# print "For year ",sighted_at_year,"States are - ",metorite_states
		if state_name in state_codes and state_codes[state_name] in metorite_states:
			df_meteor_by_state = df_meteor_by_year.loc[df_meteor_by_year['state'] == state_codes[state_name]]
			for i, meteor_row in df_meteor_by_state.iterrows():
				meteor_coord = (meteor_row['reclat'], meteor_row['reclong'])
				distance = get_distance_bw_coord(ufo_coord, meteor_coord)
				if distance <= min_dist:
					min_dist = distance
					met_name = meteor_row['name']
			meteor_name.append(met_name)
			if math.isinf(distance):
				distance_to_meteor.append("NA")
				reason.append("No Meteorites in state for the year")
				metorite_lat.append("NA")
				metorite_long.append("NA")
			else:# Mark entries as success, if and entry can be found in the same state and around the same time.
				distance_to_meteor.append(min_dist)
				reason.append("Success")
				metorite_lat.append(meteor_row['reclat'])
				metorite_long.append(meteor_row['reclong'])

		else:#if the metorite state is not present in the ufo data set
			distance_to_meteor.append("NA")
			meteor_name.append("NA")
			reason.append("No Meteorites in state for the year")
			metorite_lat.append("NA")
			metorite_long.append("NA")
	else:#if sighted at year is not present in the metorite data set
		distance_to_meteor.append("NA")
		meteor_name.append("NA")
		reason.append("Year is not present")
		metorite_lat.append("NA")
		metorite_long.append("NA")

print len(meteor_name)
print len(distance_to_meteor)
print len(reason)
print len(metorite_lat)
print len(metorite_long)

ufo_sighting['meteor_name'] = meteor_name
ufo_sighting['distance_to_meteor'] = distance_to_meteor
ufo_sighting['reason'] = reason
ufo_sighting['metorite_lat'] = metorite_lat
ufo_sighting['metorite_long'] = metorite_long
ufo_sighting.to_csv('reference_w_meteorite.csv', index=False)
