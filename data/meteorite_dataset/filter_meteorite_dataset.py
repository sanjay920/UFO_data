import pandas as pd
import json

metorite_data = pd.read_csv('meteorite-landings.csv')

state_codes = {}
with open('../utility_data/us_states_isocode.txt') as file:
	state_codes = json.load(file)

bounding_box = {}
with open('../utility_data/bounding_box.txt') as f:
    bounding_box = json.load(f)

state = []
for index, row in metorite_data.iterrows():
	lat = row['reclat']
	lon = row['reclong']

	state_name = ""
	for key in bounding_box:
		bbox = bounding_box[key]
		if len(bbox) > 0 and (lat >= bbox[0] and lat<= bbox[1]) and (lon >= bbox[2] and lon<= bbox[3]):
			state_name = key
	state.append(state_name)

metorite_data['state'] = state

metorite_data.to_csv('us_metorite_landings_with_states.csv')
