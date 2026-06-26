import pandas as pd
import numpy as np

# Load train and test datasets
train = pd.read_csv("train_final.csv")
test = pd.read_csv("test_final.csv")   # or test_final.csv if not cleaned yet

# --------------------------------------------------
# Find rows where all three soil components are zero
# --------------------------------------------------

mask = (
    (test["sand"] == 0) &
    (test["silt"] == 0) &
    (test["clay"] == 0)
)

print(f"Rows with invalid soil values: {mask.sum()}")

# --------------------------------------------------
# Replace those values with NaN
# --------------------------------------------------

test.loc[mask, ["sand", "silt", "clay"]] = np.nan

# --------------------------------------------------
# Fill using TRAIN dataset medians
# --------------------------------------------------

for col in ["sand", "silt", "clay"]:
    median = train[col].median()
    test[col] = test[col].fillna(median)

# --------------------------------------------------
# Verify
# --------------------------------------------------

mask_after = (
    (test["sand"] == 0) &
    (test["silt"] == 0) &
    (test["clay"] == 0)
)

print(f"Rows still having all zeros: {mask_after.sum()}")

# --------------------------------------------------
# Save cleaned dataset
# --------------------------------------------------

test.to_csv("test_final.csv", index=False)

print("Cleaned test dataset saved successfully.")
