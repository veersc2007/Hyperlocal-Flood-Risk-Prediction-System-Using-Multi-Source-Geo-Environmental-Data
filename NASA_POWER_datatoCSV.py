import pandas as pd
import requests
import time
import os

# =========================
# 🌧️ NASA POWER API FUNCTION
# =========================

def get_nasa_power(lat, lon):

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOTCORR,T2M"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start=20220101"
        f"&end=20221231"
        f"&format=JSON"
    )

    try:
        r = requests.get(url, timeout=20)
        data = r.json()

        rain = data["properties"]["parameter"]["PRECTOTCORR"]
        temp = data["properties"]["parameter"]["T2M"]

        rain_avg = sum(rain.values()) / len(rain)
        temp_avg = sum(temp.values()) / len(temp)

        return rain_avg, temp_avg

    except:
        return None, None


# =========================
# 💾 CHECKPOINT FUNCTIONS
# =========================

def load_checkpoint(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return int(f.read().strip())
    return 0


def save_checkpoint(index, file):
    with open(file, "w") as f:
        f.write(str(index))


# =========================
# ⚙️ MAIN PROCESSOR
# =========================

def process_with_resume(df, output_file, checkpoint_file, name):

    start_index = load_checkpoint(checkpoint_file)
    print(f"\n🚀 [{name}] Resuming from index: {start_index}")

    # create output file if not exists
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write("lat,lon,rainfall,temperature\n")

    for i in range(start_index, len(df)):

        lat = df.loc[i, "lat"]
        lon = df.loc[i, "lon"]

        rain, temp = get_nasa_power(lat, lon)

        # skip bad API responses
        if rain is None or temp is None:
            continue

        # append immediately (no RAM storage)
        with open(output_file, "a") as f:
            f.write(f"{lat},{lon},{rain},{temp}\n")

        # save checkpoint (IMPORTANT FIX)
        save_checkpoint(i + 1, checkpoint_file)

        # progress logging
        if i % 1 == 0:
            print(f"[{name}] Processed {i}/{len(df)}")

        time.sleep(0.2)  # avoid API throttling


# =========================
# 📥 LOAD DATA
# =========================

train_df = pd.read_csv("karnataka_train_grid.csv")
test_df  = pd.read_csv("karnataka_test_grid.csv")


# =========================
# 🟢 TRAIN EXECUTION
# =========================

process_with_resume(
    train_df,
    "nasa_train_dataset.csv",
    "train_progress.txt",
    "TRAIN"
)


# =========================
# 🔴 TEST EXECUTION
# =========================

process_with_resume(
    test_df,
    "nasa_test_dataset.csv",
    "test_progress.txt",
    "TEST"
)


print("\n✅ NASA POWER extraction complete (TRAIN + TEST fixed)")
