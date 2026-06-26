import pandas as pd
import numpy as np

# ==========================================================
# LOAD TRAIN & TEST DATA
# ==========================================================

train = pd.read_csv("train_final.csv")
test = pd.read_csv("test_final.csv")

print("="*60)
print("Original Test Shape:", test.shape)
print("="*60)

# ==========================================================
# CLEAN COLUMN NAMES
# ==========================================================

train.columns = train.columns.str.strip()
test.columns = test.columns.str.strip()

# ==========================================================
# REMOVE DUPLICATE ROWS FROM TEST
# ==========================================================

duplicates = test.duplicated().sum()
print(f"Duplicate rows removed: {duplicates}")

test = test.drop_duplicates()

# ==========================================================
# REPLACE INVALID VALUES
# ==========================================================

invalid_values = [-32768, -9999, -99999, 999999]

train.replace(invalid_values, np.nan, inplace=True)
test.replace(invalid_values, np.nan, inplace=True)

# ==========================================================
# HANDLE NUMERIC NaN VALUES
# (Use TRAIN medians)
# ==========================================================

numeric_cols = test.select_dtypes(include=[np.number]).columns

for col in numeric_cols:

    if col in train.columns:

        median = train[col].median()

        missing = test[col].isnull().sum()

        if missing > 0:

            print(f"Filling {missing} missing values in '{col}' using train median ({median:.3f})")

            test[col] = test[col].fillna(median)

# ==========================================================
# HANDLE CATEGORICAL NaN VALUES
# (Use TRAIN mode)
# ==========================================================

categorical_cols = test.select_dtypes(include=["object"]).columns

for col in categorical_cols:

    if col in train.columns:

        mode = train[col].mode()[0]

        missing = test[col].isnull().sum()

        if missing > 0:

            print(f"Filling {missing} missing values in '{col}' using train mode ({mode})")

            test[col] = test[col].fillna(mode)

# ==========================================================
# REMOVE CONSTANT COLUMNS
# ==========================================================

constant_cols = [col for col in test.columns if test[col].nunique() <= 1]

if constant_cols:
    print("\nRemoving constant columns:")
    print(constant_cols)
    test.drop(columns=constant_cols, inplace=True)

# ==========================================================
# FINAL CHECK
# ==========================================================

print("\n" + "="*60)
print("FINAL TEST DATASET")
print("="*60)

print("Shape:", test.shape)

print("\nMissing Values:")
print(test.isnull().sum())

print("\nData Types:")
print(test.dtypes)

print("\nSummary Statistics:")
print(test.describe())

# ==========================================================
# SAVE
# ==========================================================

test.to_csv("test_final", index=False)

print("\nML-ready test dataset saved as 'test_final.csv'")
