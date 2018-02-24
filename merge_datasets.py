# NOTE : Utility code to merge airport data with original ufo dataset




import pandas as pd
import json
from geopy.distance import vincenty
from collections import defaultdict

us_ufo_data = pd.read_csv('ufo_address_processed.csv', encoding='ISO-8859-1')
airport_data = pd.read_csv('input_data/airports.csv', encoding='ISO-8859-1')
airport_data = airport_data[airport_data['iso_country'] == 'US']

us_state_codes = {}

# State names to ISO region codes
with open('input_data/us_states_isocode.txt') as file:
    us_state_codes = json.load(file)


# To compute distance between two coordinates
def get_distance_bw_coord(loc1, loc2):
    try:
        dist = vincenty(loc1, loc2).miles
        return dist
    except:
        return float('inf')


# Filter airport by state
def get_airport_by_state(state, AP_data):
    ap_state_data = AP_data.loc[AP_data['iso_region'] == state]
    return ap_state_data


# NOTE : Use the below code to test the functions
# dc_airport = get_airport_by_state('US-DC', airport_data)
# print dc_airport.shape
#
# for index, row in dc_airport.iterrows():
#     print row['iso_region']

# iowa_ufo = (41.6612561, -91.5299106)
# iowa_airport = (41.31689835, -93.09600067)
#
# print get_distance_bw_coord(iowa_ufo, iowa_airport)

# The below lists are the new columns that will be added
airport_names = []
minimum_distances = []
airport_state = []

# For caching
airport_name = ""
city_airport_map = dict()

for location in us_ufo_data['location']:
    frame = us_ufo_data.loc[us_ufo_data['location'] == location]
    frame = frame.iloc[0]
    min_airport_detail = []
    state = frame['state']
    if state in us_state_codes:
        state = us_state_codes[state]

        ufo_coordinates = (frame['latitude'], frame['longitude'])

        min_distance = float('inf')
        closest_airport = ""
        state_name = ""
        airport_data_state = get_airport_by_state(state, airport_data)

        for index, airport_detail in airport_data_state.iterrows():
            ufo_coord = (frame['latitude'], frame['longitude'])
            airport_coord = (airport_detail['latitude_deg'], airport_detail['longitude_deg'])
            distance = get_distance_bw_coord(ufo_coord, airport_coord)
            if distance < min_distance:
                min_airport_detail = [distance, airport_detail['name'], airport_detail['iso_region'], airport_detail['iso_country']]
                min_distance = distance
                closest_airport = airport_detail['name']
                state_name = airport_detail['iso_region']

        airport_names.append(closest_airport)
        minimum_distances.append(min_distance)
        airport_state.append(state_name)

    else:
        airport_names.append("NA")
        minimum_distances.append("inf")
        airport_state.append("NA")
        print "us state code not present - ",state

    city_airport_map[location] = min_airport_detail

new_df = pd.DataFrame(us_ufo_data, columns=list(us_ufo_data))
new_df['airport_names'] = airport_names
new_df['minimum_distances'] = minimum_distances
new_df['airport_state'] = airport_state

new_df.to_csv('airport_merged.csv', encoding='utf-8', index='False')

print new_df.shape

# print city_airport_map
