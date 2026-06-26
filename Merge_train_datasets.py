import pandas as pd

# ==========================
# LOAD DATASETS
# ==========================

nasa = pd.read_csv("nasa_train_dataset.csv")
soil = pd.read_csv("soil_train.csv")
river = pd.read_csv("train_with_river.csv")
elevation = pd.read_csv("karnataka_train_with_elevation.csv")
slope = pd.read_csv("karnataka_train_with_slope.csv")

# ==========================
# REMOVE DUPLICATE COORDINATES
# ==========================

soil = soil.drop_duplicates(subset=["Latitude", "Longitude"])
river = river.drop_duplicates(subset=["Latitude", "Longitude"])
elevation = elevation.drop_duplicates(subset=["Latitude", "Longitude"])
slope = slope.drop_duplicates(subset=["Latitude", "Longitude"])

# ==========================
# KEEP ONLY REQUIRED COLUMNS
# ==========================

# Replace these column names with the actual names in your files if needed
soil = soil[["Latitude", "Longitude", "clay" , "sand" , "silt"]]

river = river[["Latitude", "Longitude", "river_distance"]]

elevation = elevation[["Latitude", "Longitude", "Elevation"]]

slope = slope[["Latitude", "Longitude", "Slope"]]

# ==========================
# MERGE
# ==========================

train = nasa.merge(
    soil,
    on=["Latitude", "Longitude"],
    how="left"
)

train = train.merge(
    river,
    on=["Latitude", "Longitude"],
    how="left"
)

train = train.merge(
    elevation,
    on=["Latitude", "Longitude"],
    how="left"
)

train = train.merge(
    slope,
    on=["Latitude", "Longitude"],
    how="left"
)

# ==========================
# SAVE
# ==========================

train.to_csv("train_final.csv", index=False)

print("===================================")
print("Training dataset merged successfully!")
print("Rows :", len(train))
print("Columns :", len(train.columns))
print("Saved as Train_final.csv")
print("===================================")

print("\nMissing values:")
print(train.isnull().sum())
