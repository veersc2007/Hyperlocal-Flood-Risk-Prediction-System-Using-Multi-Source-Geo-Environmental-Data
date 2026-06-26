import pandas as pd
import numpy as np

# ==========================================================
# LOAD DATASETS
# ==========================================================

train = pd.read_csv("train_final.csv")
test = pd.read_csv("test_final.csv")

# ==========================================================
# CLEAN COLUMN NAMES
# ==========================================================

train.columns = train.columns.str.strip()
test.columns = test.columns.str.strip()

# ==========================================================
# REMOVE DUPLICATE ROWS
# ==========================================================

test.drop_duplicates(inplace=True)

# ==========================================================
# REPLACE INVALID VALUES
# ==========================================================

invalid_values = [-32768, -9999, -99999, 999999]

train.replace(invalid_values, np.nan, inplace=True)
test.replace(invalid_values, np.nan, inplace=True)

# ==========================================================
# ELEVATION CHECK
# ==========================================================

# If your study area should not contain elevations <= 0,
# treat them as invalid.

elev_mask = test["Elevation"] <= 0

print("Invalid Elevation Rows:", elev_mask.sum())

test.loc[elev_mask, "Elevation"] = np.nan

# ==========================================================
# SLOPE CHECK
# ==========================================================

# Negative slopes are impossible.
# Keep slope = 0 because perfectly flat land exists.

slope_mask = test["Slope"] < 0

print("Invalid Slope Rows:", slope_mask.sum())

test.loc[slope_mask, "Slope"] = np.nan

# ==========================================================
# IMPUTE NUMERIC VALUES USING TRAIN MEDIANS
# ==========================================================

numeric_cols = train.select_dtypes(include=np.number).columns

for col in numeric_cols:

    if col == "Flood_Score":
        continue

    if col in test.columns:

        median = train[col].median()

        test[col] = test[col].fillna(median)

# ==========================================================
# IMPUTE CATEGORICAL VALUES USING TRAIN MODE
# ==========================================================

categorical_cols = train.select_dtypes(include="object").columns

for col in categorical_cols:

    if col in test.columns:

        mode = train[col].mode()[0]

        test[col] = test[col].fillna(mode)

# ==========================================================
# FINAL CHECK
# ==========================================================

print("\nRemaining Missing Values:")
print(test.isnull().sum())

print("\nFinal Dataset Shape:", test.shape)

# ==========================================================
# SAVE
# ==========================================================

test.to_csv("test_final.csv", index=False)

print("\nTest ML dataset saved successfully.")
