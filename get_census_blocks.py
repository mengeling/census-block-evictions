import sys
import json
import requests
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import config as c


def get_centroid(row):
    n = row.get("north")
    s = row.get("south")
    e = row.get("east")
    w = row.get("west")
    return Point([n - (n - s) / 2, e - (e - w) / 2])


def create_polygon(coordinates):
    lst_polygon = []
    for i, coord in enumerate(coordinates):
        if i % 2 == 0:
            lst = [coord]
        else:
            lst.append(coord)
            lst_polygon.append(lst)
    return Polygon(lst_polygon)


def load_data(states):
    lst_dfs = []
    for i, state in enumerate(states):
        f_csv = "https://eviction-lab-data-downloads.s3.amazonaws.com/{}/block-groups.csv".format(state)
        f_json = "https://eviction-lab-data-downloads.s3.amazonaws.com/{}/block-groups.geojson".format(state)
        lst_dfs.append(pd.read_csv(f_csv))
        if i == 0:
            json_data = requests.get(f_json).json()
        else:
            json_data["features"] += requests.get(f_json).json()["features"]
    df_csv = pd.concat(lst_dfs)
    df_json = pd.DataFrame(json_data["features"])
    return df_csv, df_json, json_data


if __name__ == "__main__":

    # Loop through each city and get the relevant states and coordinates
    for city, v in c.city_lookup.items():
        states = v[0]
        coordinates = v[1]

        # Load geojson and csv data and create polygon for area of interest
        df_csv, df_json, json_data = load_data(states)
        polygon = create_polygon(coordinates)

        # Filter to the rows we care about
        df_json["centroid"] = df_json["properties"].apply(get_centroid)
        df_json_filtered = df_json[df_json["centroid"].apply(lambda x: polygon.contains(x))]
        df_json_filtered["GEOID"] = df_json_filtered["properties"].apply(lambda x: x.get("GEOID"))

        # Recreate the geojson with the filtered rows and filter CSV df
        json_filtered = json_data.copy()
        json_filtered["features"] = df_json_filtered.drop(["centroid", "GEOID"], axis=1).to_dict("records")
        df_csv_filtered = df_csv[df_csv["GEOID"].isin(df_json_filtered["GEOID"])]

        # Write the data locally
        df_csv_filtered.to_csv("data/{}.csv".format(city), index=False)
        with open("data/{}.geojson".format(city), "w") as f:
            json.dump(json_filtered, f)
