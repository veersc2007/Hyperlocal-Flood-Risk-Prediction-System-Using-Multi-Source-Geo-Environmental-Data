import h5py
import numpy as np
import pandas as pd

# =========================
# LOAD YOUR GRIDS
# =========================

train_df = pd.read_csv("karnataka_train_grid.csv")
test_df  = pd.read_csv("karnataka_test_grid.csv")

# =========================
# OPEN MODIS FILES
# =========================

files = [
    "MCD12Q1.h24v06.hdf",
    "MCD12Q1.h25v06.hdf",
    "MCD12Q1.h26v06.hdf"
]

# =========================
# READ LAND COVER LAYER
# =========================

def load_landcover(file):
    f = h5py.File(file, 'r')

    # MODIS dataset path (important)
    data = f["MOD12Q1/LC_Type1_1"]

    return np.array(data)


# Combine tiles (simplified mosaic)
lc_tiles = [load_landcover(f) for f in files]

# stack (you can improve later with geo alignment)
landcover_map = lc_tiles[0]  # start simple


# =========================
# FUNCTION: GET VALUE
# =========================

def get_lc_value(lat, lon):
    """
    Simplified lookup (grid approximation)
    """

    # convert lat/lon to pseudo index (approx method)
    i = int((lat - 12) * 100)
    j = int((lon - 74) * 100)

    i = max(0, min(i, landcover_map.shape[0]-1))
    j = max(0, min(j, landcover_map.shape[1]-1))

    return int(landcover_map[i][j])


# =========================
# PROCESS FUNCTION
# =========================

def process(df, name):

    lc_vals = []

    for idx in range(len(df)):

        lat = df.loc[idx, "lat"]
        lon = df.loc[idx, "lon"]

        try:
            val = get_lc_value(lat, lon)
        except:
            val = np.nan

        lc_vals.append(val)

        if idx % 100 == 0:
            print(f"{name}: processed {idx}/{len(df)}")

    df["landcover"] = lc_vals
    return df


# =========================
# RUN TRAIN
# =========================

print("\n🚀 TRAIN")
train_df = process(train_df, "TRAIN")
train_df.to_csv("train_with_landcover.csv", index=False)

# =========================
# RUN TEST
# =========================

print("\n🚀 TEST")
test_df = process(test_df, "TEST")
test_df.to_csv("test_with_landcover.csv", index=False)

print("\n✅ DONE")
