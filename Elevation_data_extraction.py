import pandas as pd
import rasterio

# Load training data
df = pd.read_csv(r"karnataka_train_grid.csv")

# Open DEM
with rasterio.open("Karnataka_dem.tif") as dem:

    coords = [(lon, lat) for lon, lat in zip(df["Longitude"], df["Latitude"])]

    elevations = []

    for value in dem.sample(coords):
        elevations.append(float(value[0]))

df["Elevation"] = elevations

df.to_csv("karnataka_train_with_elevation.csv", index=False)

print("Done!")

# Load testing data
df = pd.read_csv(r"karnataka_test_grid.csv")

# Open DEM
with rasterio.open("Karnataka_dem.tif") as dem:

    coords = [(lon, lat) for lon, lat in zip(df["Longitude"], df["Latitude"])]

    elevations = []

    for value in dem.sample(coords):
        elevations.append(float(value[0]))

df["Elevation"] = elevations

df.to_csv("karnataka_test_with_elevation.csv", index=False)

print("Done!")
