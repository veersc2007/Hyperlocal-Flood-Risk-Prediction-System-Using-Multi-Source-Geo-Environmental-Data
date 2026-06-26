import pandas as pd
import rasterio

df = pd.read_csv(r"karnataka_train_grid.csv")

with rasterio.open("Karnataka_slope.tif") as src:

    coords = [(lon, lat) for lon, lat in zip(df["Longitude"], df["Latitude"])]

    df["Slope"] = [float(v[0]) for v in src.sample(coords)]

df.to_csv("karnataka_train_with_slope.csv", index=False)

print("Training slope extraction complete.")

df = pd.read_csv("karnataka_test_grid.csv")

with rasterio.open("Karnataka_slope.tif") as src:

    coords = [(lon, lat) for lon, lat in zip(df["Longitude"], df["Latitude"])]

    df["Slope"] = [float(v[0]) for v in src.sample(coords)]

df.to_csv("karnataka_test_with_slope.csv", index=False)

print("Testing slope extraction complete.")
