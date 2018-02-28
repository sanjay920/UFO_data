# NOTE
# utitlity code to extract coordinates / city / state for each location in the data set
# Make sure you have these packages installed before running this code
# I have imported the tsv file in excel and saved it as a csv
# Why? Mainly because the original tsv had formatting issues and was unable to parse them in pandas

# TODO : Need to clean up these packages and only keep the ones which are needed
import pandas as pd
import re
import math
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep
import datetime

# change the location of your input files here.
DATASET_LOCATION = "../reference.csv"
OUTPUT_FILE_NAME = "geo_location_appended.csv"
LOCATION_CACHE = "geocoded_location_dict.txt"

# utility function to write the results to local cache
def writeToCache(location_data):
    with open(LOCATION_CACHE, 'w') as file:
        file.write(json.dumps(location_data))


# given location name fetch the coordinates for plotting
def getLatLong(location_name, processed_addr):
    global count
    count += 1
    if isinstance(location_name, str):
        geolocator = Nominatim()
        # IF the location is already fetched, return it from the cache
        if location_name in processed_addr:
            return processed_addr[location_name]
        else:#IF the location is not fetched, then use geolocator to fetch the location
            try:
                # Need a time out of 1 second between requests to prevent geocode from
                sleep(1)
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
                    with open('local_cache.txt', 'a+') as file:
                        file.write("{0}:{1}\n".format("{"+location_name,json.dumps(processed_addr[location_name]) + "}"))
                    return [lat, lon, city, state, country]
                else:
                    ""
            except GeocoderTimedOut:
                writeToCache(processed_addr)
                sys.exit
            except:
                writeToCache(processed_addr)
                sys.exit
    else:
        return ""



# Function to build csv from cache
def build_coordinates_dataset(data, processed_addr):
    df = pd.DataFrame(data, columns = ['sighted_at','reported_at','location','shape','duration','description'])
    latitude = []
    longitude = []
    state = []
    city = []
    country = []
    for loc in data['location']:
        if loc in processed_addr:
            addr = processed_addr[loc]
            latitude.append(addr[0])
            longitude.append(addr[1])
            state.append(addr[2])
            city.append(addr[3])
            country.append(addr[4])
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

    print df.shape

    df.to_csv(OUTPUT_FILE_NAME, index=False, encoding='utf-8')



data = pd.read_csv(DATASET_LOCATION)
# df = pd.DataFrame(data, columns = ['sighted_at','reported_at','location','shape','duration','description'])


# Loading the contents of location cache into a dictionary
processed_addr = {}
try:
    fpointer = open(LOCATION_CACHE, 'r')
    processed_addr = json.load(fpointer)
except:
    processed_addr = {}

# Load the adresses fetched so far into the cache
build_coordinates_dataset(data, processed_addr)

# NOTE : The below commented code was used to initially build the cache and write the final datafram as a csv(With geo locations updated)
# latitude = []
# longitude = []
# state = []
# city = []
# country = []
# count = 0
#
# for x in data['location']:
#     # print "Count is ", count
#     location_details = getLatLong(x, processed_addr)
#     print location_details
#     # lat, lon, city, state, country
#     if location_details != "" and location_details is not None:
#         latitude.append(location_details[0])
#         longitude.append(location_details[1])
#         city.append(location_details[2])
#         state.append(location_details[3])
#         country.append(location_details[4])
#     else:
#         latitude.append("NA")
#         longitude.append("NA")
#         state.append("NA")
#         city.append("NA")
#         country.append("NA")
#
# # write all the processed addresses to the cache
# writeToCache(processed_addr)
#
# # Append the additional columns inferred from geo code to the data frame
# df['latitude'] = latitude
# df['longitude'] = longitude
# df['city'] = city
# df['state'] = state
# df['country'] = country
#
# df.to_csv(OUTPUT_FILE_NAME, index=False)
