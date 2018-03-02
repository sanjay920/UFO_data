Main Folder: CS599-UFOs-PA1

Sub Folders:
1. assignment_description
2. cached_data- contains cached data for locations (created when extracting location co-ordinates using geopy)
3. d3_work- contains code to generate d3 visualizations
4. data- contains datasets used 
5. merge_data- contains final dataset

Order of execution:
1) Follow /data/initial_cleaning to get reference.csv

2) Follow /data/geocoded_location to get reference_w_loc.csv

3) Use /data/shapes_cleaning to attempt to extract shape from description for UFO sightings that did not report a shape -- this uses and overwrites reference_w_loc.csv

4) Follow /data/airport_dataset to produce reference_w_airports.csv

5) Follow /data/sports_dataset to produce reference_w_sports.csv

6) Follow /data/meteorite_dataset to produce reference_w_meteorite.csv
