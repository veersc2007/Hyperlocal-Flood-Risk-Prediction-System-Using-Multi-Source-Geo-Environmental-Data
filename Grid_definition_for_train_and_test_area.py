import numpy as np
import pandas as pd

# =========================
# 🗺️ 1. KARNATAKA BOUNDING REGIONS
# =========================

# 🟢 TRAIN REGION (Interior Karnataka)
train_bbox = {
    "lat_min": 12.0,
    "lat_max": 16.5,
    "lon_min": 75.0,
    "lon_max": 78.5
}

# 🔴 TEST REGION (Coastal Karnataka)
test_bbox = {
    "lat_min": 12.5,
    "lat_max": 15.5,
    "lon_min": 74.0,
    "lon_max": 75.5
}

# =========================
# ⚙️ 2. GRID RESOLUTION
# =========================

resolution = 0.1  # 0.1 degree grid (~10km)

# =========================
# 🟢 3. FUNCTION TO CREATE GRID
# =========================

def create_grid(bbox, name):
    lat_vals = np.arange(bbox["lat_min"], bbox["lat_max"], resolution)
    lon_vals = np.arange(bbox["lon_min"], bbox["lon_max"], resolution)

    grid = []

    for lat in lat_vals:
        for lon in lon_vals:
            grid.append([lat, lon])

    df = pd.DataFrame(grid, columns=["lat", "lon"])
    df["region"] = name

    return df

# =========================
# 🟢 4. CREATE TRAIN + TEST GRIDS
# =========================

train_df = create_grid(train_bbox, "train")
test_df = create_grid(test_bbox, "test")

# =========================
# 📊 5. BASIC INFO
# =========================

print("TRAIN GRID SHAPE:", train_df.shape)
print("TEST GRID SHAPE:", test_df.shape)

print("\nSample TRAIN data:")
print(train_df.head())

print("\nSample TEST data:")
print(test_df.head())

# =========================
# 💾 6. SAVE FILES
# =========================

train_df.to_csv("karnataka_train_grid.csv", index=False)
test_df.to_csv("karnataka_test_grid.csv", index=False)

print("\nFiles saved successfully!")
