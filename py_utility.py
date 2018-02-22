# NOTE
# utitlity code to extract coordinates / city / state for each location in the data set
# Make sure you have these packages installed before running this code
# I have imported the tsv file in excel and saved it as a csv
# Why? Mainly because the original tsv had formatting issues and was unable to parse them in pandas


import pandas as pd
import re
import math
from geopy.geocoders import Nominatim
from time import sleep
import datetime


DATASET_LOCATION = "chimps_16154-2010-10-20_14-33-35/test_ufo_data.csv"
OUTPUT_FILE_NAME = "ufo_address_processed.csv"

# given location name fetch the coordinates for plotting
def getLatLong(location_name, processed_addr):
    # Need a time out of 1 second between requests
    sleep(3)
    if isinstance(location_name, str):
        geolocator = Nominatim()
        if location_name in processed_addr:
            return processed_addr[location_name]
        else:
            location = geolocator.geocode(location_name, addressdetails=True)
            if location:
                loc_json = location.raw
                lat = location.latitude
                lon = location.longitude
                state = "NA"
                city = "NA"
                country = "NA"
                try:
                    state = loc_json['address']['state'] or "NA"
                    city = loc_json['address']['city'] or "NA"
                    country = loc_json['address']['country_code'] or "NA"
                except:
                    print "key error ",loc_json
                processed_addr[location_name] = [lat, lon, city, state, country]
                return [lat, lon, city, state, country]
            else:
                ""
    else:
        return ""

data = pd.read_csv(DATASET_LOCATION)
df = pd.DataFrame(data, columns = ['sighted_at','reported_at','location','shape','duration','description'])

processed_addr = {}
latitude = []
longitude = []
state = []
city = []
country = []

for x in data['location']:
    location_details = getLatLong(x, processed_addr)
    print location_details
    # lat, lon, city, state, country
    if location_details != "" and location_details is not None:
        latitude.append(location_details[0])
        longitude.append(location_details[1])
        city.append(location_details[2])
        state.append(location_details[3])
        country.append(location_details[4])
    else:
        latitude.append("NA")
        longitude.append("NA")
        state.append("NA")
        city.append("NA")
        country.append("NA")

# coordinates = [getLatLong(x, processed_addr) for x in data['location']]
# df['coordinates'] = coordinates

df['latitude'] = latitude
df['longitude'] = longitude
df['city'] = city
df['state'] = state
df['country'] = country

df.to_csv(OUTPUT_FILE_NAME, index=False)
#
# print coordinates
