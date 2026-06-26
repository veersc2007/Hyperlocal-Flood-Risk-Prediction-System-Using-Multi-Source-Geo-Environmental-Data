import pandas as pd
import rasterio
import os
import time

# =========================
# 📥 LOAD GRID
# =========================

train_df = pd.read_csv("karnataka_train_grid.csv")
test_df  = pd.read_csv("karnataka_test_grid.csv")


# =========================
# 🟤 LOAD RASTERS
# =========================

clay_raster = rasterio.open("clay.tif")
sand_raster = rasterio.open("sand.tif")
silt_raster = rasterio.open("silt.tif")


# =========================
# 🌍 SAMPLE FUNCTION
# =========================

def get_soil_features(lat, lon):

    try:
        clay = list(clay_raster.sample([(lon, lat)]))[0][0]
        sand = list(sand_raster.sample([(lon, lat)]))[0][0]
        silt = list(silt_raster.sample([(lon, lat)]))[0][0]

        return clay, sand, silt

    except:
        return None, None, None


# =========================
# 💾 CHECKPOINT SYSTEM
# =========================

def load_checkpoint(file):
    if os.path.exists(file):
        return int(open(file).read().strip())
    return 0


def save_checkpoint(i, file):
    with open(file, "w") as f:
        f.write(str(i))


# =========================
# ⚙️ PROCESS FUNCTION
# =========================

def process_soil(df, output_file, checkpoint_file, name):

    start = load_checkpoint(checkpoint_file)
    print(f"\n🚀 [{name}] Resuming from index: {start}")

    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write("lat,lon,clay,sand,silt\n")

    for i in range(start, len(df)):

        lat = df.loc[i, "lat"]
        lon = df.loc[i, "lon"]

        clay, sand, silt = get_soil_features(lat, lon)

        if None in (clay, sand, silt):
            continue

        with open(output_file, "a") as f:
            f.write(f"{lat},{lon},{clay},{sand},{silt}\n")

        save_checkpoint(i + 1, checkpoint_file)

        if i % 100 == 0:
            print(f"[{name}] Processed {i}/{len(df)}")

        time.sleep(0.01)


# =========================
# 🚀 RUN TRAIN + TEST
# =========================

process_soil(
    train_df,
    "soil_train.csv",
    "soil_train_ckpt.txt",
    "TRAIN"
)

process_soil(
    test_df,
    "soil_test.csv",
    "soil_test_ckpt.txt",
    "TEST"
)

print("\n✅ Soil feature extraction complete!")
