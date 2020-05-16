# Census Block Evictions

This repository gives users the ability to scrape eviction data from https://evictionlab.org/ at the most granular level (census block) in order to analyze particular locations of interest in the US.

To collect the right census block data, start by creating a polygon perimeter for the location of interest using a website like http://apps.headwallphotonics.com/ as shown below.

![Alt text](img/dc_hpi_polygon.png)

Next, add the location's name as a new key in `config.py`, and make the value a list where the first value in the list is a list of all the states (two-letter state abbreviations) inside the polygon, and the second value is a list of the polygon's latitudes and longitudes. The entry for Washington DC is shown below.

![Alt text](img/dc_config.png)

Once all of the desired locations have been added to `config.py`, run `python get_census_blocks.py` to generate a CSV and .geojson file for each of the locations in the data directory. The CSV will have the eviction data for all of the locations in the polygon, and the .geojson file can be uploaded to a website like https://mapshaper.org/ to visually confirm the right census blocks were selected as shown below for Washington DC.

![Alt text](img/dc_mapshaper.png)
