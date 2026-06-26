import pandas as pd
import numpy as np

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("train_final.csv")

print("="*60)
print("Original Dataset Shape:", df.shape)
print("="*60)

# ======================================================
# CLEAN COLUMN NAMES
# ======================================================

df.columns = df.columns.str.strip()

# ======================================================
# REMOVE DUPLICATE ROWS
# ======================================================

duplicates = df.duplicated().sum()
print(f"Duplicate rows found: {duplicates}")

df.drop_duplicates(inplace=True)

# ======================================================
# REPLACE INVALID VALUES WITH NaN
# ======================================================

invalid_values = [-32768, -9999, 999999, -99999]

df.replace(invalid_values, np.nan, inplace=True)

# ======================================================
# COUNT MISSING VALUES BEFORE IMPUTATION
# ======================================================

print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

# ======================================================
# HANDLE NUMERIC COLUMNS
# ======================================================

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:

    missing = df[col].isnull().sum()

    if missing > 0:

        median = df[col].median()

        print(f"Filling {missing} missing values in '{col}' with median ({median:.3f})")

        df[col].fillna(median, inplace=True)

# ======================================================
# HANDLE CATEGORICAL COLUMNS
# ======================================================

categorical_cols = df.select_dtypes(include=["object"]).columns

for col in categorical_cols:

    missing = df[col].isnull().sum()

    if missing > 0:

        mode = df[col].mode()[0]

        print(f"Filling {missing} missing values in '{col}' with mode ({mode})")

        df[col].fillna(mode, inplace=True)

# ======================================================
# REMOVE CONSTANT COLUMNS
# ======================================================

constant_cols = []

for col in df.columns:

    if df[col].nunique() <= 1:
        constant_cols.append(col)

if len(constant_cols) > 0:

    print("\nRemoving constant columns:")
    print(constant_cols)

    df.drop(columns=constant_cols, inplace=True)

# ======================================================
# FINAL CHECK
# ======================================================

print("\n" + "="*60)
print("FINAL DATASET")
print("="*60)

print("Shape:", df.shape)

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nSummary Statistics:")
print(df.describe())

# ======================================================
# SAVE
# ======================================================

df.to_csv("train_final.csv", index=False)

print("\nML-ready dataset saved as 'train_ml_ready.csv'")
