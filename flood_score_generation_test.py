import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ======================================================
# LOAD TRAIN DATASET
# ======================================================

df = pd.read_csv("test_final.csv")

# ======================================================
# NORMALIZE FEATURES
# ======================================================

scaler = MinMaxScaler()

# Higher value = Higher flood risk
higher_risk = ["rainfall", "clay", "silt"]

# Lower value = Higher flood risk
lower_risk = ["river_distance", "Elevation", "Slope", "sand"]

# Normalize higher-risk features
for col in higher_risk:
    df[col + "_norm"] = scaler.fit_transform(df[[col]])

# Normalize lower-risk features and invert them
for col in lower_risk:
    df[col + "_risk"] = 1 - scaler.fit_transform(df[[col]])

# ======================================================
# COMPUTE FLOOD SUSCEPTIBILITY INDEX (FSI)
# ======================================================

df["Flood_Index"] = (
      0.35 * df["rainfall_norm"]
    + 0.20 * df["river_distance_risk"]
    + 0.15 * df["Elevation_risk"]
    + 0.15 * df["Slope_risk"]
    + 0.08 * df["clay_norm"]
    + 0.04 * df["sand_risk"]
    + 0.03 * df["silt_norm"]
)

# ======================================================
# CREATE FLOOD SCORE (0–3)
# ======================================================

q1 = df["Flood_Index"].quantile(0.25)
q2 = df["Flood_Index"].quantile(0.50)
q3 = df["Flood_Index"].quantile(0.75)

def assign_score(x):

    if x <= q1:
        return 0

    elif x <= q2:
        return 1

    elif x <= q3:
        return 2

    else:
        return 3

df["Flood_Score"] = df["Flood_Index"].apply(assign_score)

# ======================================================
# REMOVE TEMPORARY COLUMNS
# ======================================================

cols_to_remove = [col for col in df.columns
                  if col.endswith("_norm") or col.endswith("_risk")]

df.drop(columns=cols_to_remove, inplace=True)

# ======================================================
# SAVE DATASET
# ======================================================

df.to_csv("test_final.csv", index=False)

# ======================================================
# SUMMARY
# ======================================================

print("="*60)
print("Flood Score Distribution")
print("="*60)

print(df["Flood_Score"].value_counts().sort_index())

print("\nFlood Index Statistics")
print(df["Flood_Index"].describe())

print("\nDataset saved as:")
print("train_with_flood_score.csv")
