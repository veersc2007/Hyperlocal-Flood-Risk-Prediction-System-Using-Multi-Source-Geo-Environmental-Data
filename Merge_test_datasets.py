import pandas as pd
import numpy as np

# =====================================================
# LOAD DATASETS
# =====================================================

nasa = pd.read_csv("nasa_test_dataset.csv")
soil = pd.read_csv("soil_test.csv")
river = pd.read_csv("test_with_river.csv")
elevation = pd.read_csv("karnataka_test_with_elevation.csv")
slope = pd.read_csv("karnataka_test_with_slope.csv")

# =====================================================
# CLEAN COLUMN NAMES
# =====================================================

for df in [nasa, soil, river, elevation, slope]:
    df.columns = df.columns.str.strip()

# =====================================================
# ROUND COORDINATES
# =====================================================

for df in [nasa, soil, river, elevation, slope]:
    df["Latitude"] = df["Latitude"].round(6)
    df["Longitude"] = df["Longitude"].round(6)

# =====================================================
# REMOVE DUPLICATE COORDINATES
# =====================================================

soil = soil.drop_duplicates(subset=["Latitude", "Longitude"])
river = river.drop_duplicates(subset=["Latitude", "Longitude"])
elevation = elevation.drop_duplicates(subset=["Latitude", "Longitude"])
slope = slope.drop_duplicates(subset=["Latitude", "Longitude"])

# =====================================================
# MERGE DATASETS
# =====================================================

test = nasa.merge(
    soil,
    on=["Latitude", "Longitude"],
    how="left"
)

test = test.merge(
    river,
    on=["Latitude", "Longitude"],
    how="left"
)

test = test.merge(
    elevation,
    on=["Latitude", "Longitude"],
    how="left"
)

test = test.merge(
    slope,
    on=["Latitude", "Longitude"],
    how="left"
)

print("Merged Shape:", test.shape)

# =====================================================
# REPLACE INVALID VALUES
# =====================================================

invalid_values = [-32768, -9999, -99999, 999999]

test.replace(invalid_values, np.nan, inplace=True)

# =====================================================
# HANDLE NUMERIC NaN VALUES
# =====================================================

numeric_cols = test.select_dtypes(include=np.number).columns

for col in numeric_cols:

    if test[col].isnull().sum() > 0:

        median = test[col].median()

        print(f"Filling {col} with median = {median}")

        test[col] = test[col].fillna(median)

# =====================================================
# HANDLE CATEGORICAL NaN VALUES
# =====================================================

categorical_cols = test.select_dtypes(include="object").columns

for col in categorical_cols:

    if test[col].isnull().sum() > 0:

        mode = test[col].mode()[0]

        test[col] = test[col].fillna(mode)

# =====================================================
# REMOVE DUPLICATE ROWS
# =====================================================

test = test.drop_duplicates()

# =====================================================
# REMOVE CONSTANT COLUMNS
# =====================================================

constant_cols = []

for col in test.columns:

    if test[col].nunique() <= 1:
        constant_cols.append(col)

if len(constant_cols) > 0:

    print("Removing constant columns:")

    print(constant_cols)

    test.drop(columns=constant_cols, inplace=True)

# =====================================================
# FINAL REPORT
# =====================================================

print("\nFinal Shape:", test.shape)

print("\nMissing Values:")

print(test.isnull().sum())

print("\nColumn Names:")

print(test.columns.tolist())

print("\nSummary Statistics:")

print(test.describe())

# =====================================================
# SAVE
# =====================================================

test.to_csv("test_final.csv", index=False)

print("\nML-ready test dataset saved as test_ml_ready.csv")
