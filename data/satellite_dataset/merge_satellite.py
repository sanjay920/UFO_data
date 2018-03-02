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
sat_data = pd.read_csv('satellite_filtered.csv')
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
sat_years = list(set([int(x) if not math.isnan(x) else 0 for x in sat_data['Year']]))
# metorite_years = set([int(x) for x in metorite_data['year']])
distance_to_sat = []
sat_name = []
reason = []
sat_lat = []
sat_long = []

# print metorite_years

for index, row in ufo_sighting.iterrows():
	# Cases where sighted_at is invalid
	try:
		sighted_at_year = datetime.strptime(str(row['sighted_at']), "%Y%m%d")
	except:
		# Keeping record of the error type
		distance_to_sat.append("NA")
		sat_name.append("NA")
		reason.append("Invalid time format")
		sat_lat.append("NA")
		sat_long.append("NA")
		continue
	sighted_at_year = datetime.strptime(str(row['sighted_at']), "%Y%m%d")
	state_name = row['state']
	sighted_at_year = sighted_at_year.year
	ufo_coord = (row['geocoded_latitude'], row['geocoded_longitude'])

	if int(sighted_at_year) in sat_years:
		df_sat_by_year = sat_data.loc[sat_data['Year'] == sighted_at_year]

		min_dist = float('inf')
		sat_states = list(set(df_sat_by_year['State']))
		met_name = "NA"
		# print "For year ",sighted_at_year,"States are - ",metorite_states
		if state_name in sat_states:
			df_sat_by_state = df_sat_by_year.loc[df_sat_by_year['State'] == state_name]
			print df_sat_by_state
			for i, sat_row in df_sat_by_state.iterrows():
				sat_coord = (sat_row['Latitude'], sat_row['Longitude'])
				distance = get_distance_bw_coord(ufo_coord, sat_coord)
				if distance <= min_dist:
					min_dist = distance
					met_name = sat_row['Name']
			sat_name.append(met_name)
			if math.isinf(distance):
				distance_to_sat.append("NA")
				reason.append("No Satillite launched at this time")
				sat_lat.append("NA")
				sat_long.append("NA")
			else:# Mark entries as success, if and entry can be found in the same state and around the same time.
				distance_to_sat.append(min_dist)
				reason.append("Success")
				sat_lat.append(sat_row['Latitude'])
				sat_long.append(sat_row['Longitude'])

		else:#if the metorite state is not present in the ufo data set
			distance_to_sat.append("NA")
			sat_name.append("NA")
			reason.append("No Meteorites in state for the year")
			sat_lat.append("NA")
			sat_long.append("NA")
	else:#if sighted at year is not present in the metorite data set
		distance_to_sat.append("NA")
		sat_name.append("NA")
		reason.append("Year is not present")
		sat_lat.append("NA")
		sat_long.append("NA")

print len(sat_name)
print len(distance_to_sat)
print len(reason)
print len(sat_lat)
print len(sat_long)

ufo_sighting['satellite_name'] = sat_name
ufo_sighting['distance_to_satellite'] = distance_to_sat
ufo_sighting['reason'] = reason
ufo_sighting['satellite_lat'] = sat_lat
ufo_sighting['satellite_long'] = sat_long
ufo_sighting.to_csv('reference_w_satellite.csv', index=False)
