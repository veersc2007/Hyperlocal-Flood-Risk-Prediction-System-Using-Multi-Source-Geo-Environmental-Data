import pandas as pd

df = pd.read_csv("karnataka_test_grid.csv")

# force correct column names
df = df.rename(columns={
    "lat": "Latitude",
    "lon": "Longitude"
})

# add ID column (IMPORTANT)
df.insert(0, "ID", range(1, len(df)+1))

df = df[["ID", "Latitude", "Longitude"]]

df.to_csv("appeears_test.csv", index=False)
