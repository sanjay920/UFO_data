# NOTE
# utitlity code to extract coordinates / city / state for each location in the data set
# Make sure you have these packages installed before running this code
# I have imported the tsv file in excel and saved it as a csv
# Why? Mainly because the original tsv had formatting issues and was unable to parse them in pandas


import pandas as pd
import re
import math
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep
import datetime
import sys


DATASET_LOCATION = "chimps_16154-2010-10-20_14-33-35/test_ufo_awesome.csv"
OUTPUT_FILE_NAME = "ufo_address_processed.csv"
LOCATION_CACHE = "location_cache.txt"


def writeToCache(location_data):
    with open(LOCATION_CACHE, 'w') as file:
        file.write(json.dumps(location_data))

# given location name fetch the coordinates for plotting
def getLatLong(location_name, processed_addr):
    if isinstance(location_name, str):
        geolocator = Nominatim()
        if location_name in processed_addr:
            return processed_addr[location_name]
        else:
            try:
                # Need a time out of 1 second between requests
                sleep(3)
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
            except GeocoderTimedOut:
                writeToCache(processed_addr)
                sys.exit()
    else:
        return ""

data = pd.read_csv(DATASET_LOCATION)
df = pd.DataFrame(data, columns = ['sighted_at','reported_at','location','shape','duration','description'])


processed_addr = {}
try:
    fpointer = open(LOCATION_CACHE, 'r')
    processed_addr = json.load(fpointer)
except:
    processed_addr = {}

processed_addr = pd.read_csv(LOCATION_CACHE)

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


df['latitude'] = latitude
df['longitude'] = longitude
df['city'] = city
df['state'] = state
df['country'] = country

writeToCache(processed_addr)

df.to_csv(OUTPUT_FILE_NAME, index=False)
