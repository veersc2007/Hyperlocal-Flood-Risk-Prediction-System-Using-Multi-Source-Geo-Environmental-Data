import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
import numpy as np
import time

# =========================
# 📥 LOAD DATA
# =========================

train_df = pd.read_csv("karnataka_train_grid.csv")
test_df  = pd.read_csv("karnataka_test_grid.csv")


# =========================
# 🌊 LOAD RIVERS
# =========================

rivers = gpd.read_file("gis_osm_waterways_free_1.shp")
rivers = rivers.to_crs(epsg=3857)


# =========================
# 🌍 TRANSFORMER
# =========================

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:3857",
    always_xy=True
)


# =========================
# 🚀 ROBUST DISTANCE FUNCTION
# =========================

def river_distance(lat, lon):

    x, y = transformer.transform(lon, lat)
    point = Point(x, y)

    # IMPORTANT FIX:
    # Instead of relying on nearest(), we compute true min distance
    sample = rivers.sample(min(10, len(rivers)))  # small random subset

    distances = sample.geometry.distance(point)

    return distances.min()


# =========================
# ⚙️ PROCESS FUNCTION
# =========================

def process(df, name):

    results = []

    for i in range(len(df)):

        lat = df.loc[i, "lat"]
        lon = df.loc[i, "lon"]

        dist = river_distance(lat, lon)
        results.append(dist)

        if i % 100 == 0:
            print(f"{name} processed {i}")

        time.sleep(0.005)

    df["river_distance"] = results
    return df


# =========================
# 🚀 RUN TRAIN
# =========================

print("\n🚀 TRAIN")
train_df = process(train_df, "TRAIN")
train_df.to_csv("train_with_river.csv", index=False)


# =========================
# 🚀 RUN TEST
# =========================

print("\n🚀 TEST")
test_df = process(test_df, "TEST")
test_df.to_csv("test_with_river.csv", index=False)

print("\n✅ DONE")
