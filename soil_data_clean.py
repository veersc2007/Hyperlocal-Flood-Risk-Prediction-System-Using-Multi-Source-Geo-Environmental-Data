import pandas as pd

# =========================
# 📥 INPUT FILES
# =========================

train_path = input("Enter TRAIN CSV file path: ")
test_path  = input("Enter TEST CSV file path: ")

# =========================
# 📊 LOAD DATA
# =========================

train_df = pd.read_csv(train_path)
test_df  = pd.read_csv(test_path)

print("\n✅ Files loaded successfully!")


# =========================
# 🧠 MEDIAN IMPUTATION FUNCTION
# =========================

def clean_with_median(df, name):

    print(f"\n🟢 Cleaning {name} dataset...")

    # numeric columns only
    num_cols = df.select_dtypes(include=["float64", "int64"]).columns

    for col in num_cols:

        if df[col].isna().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

            print(f"✔ Filled NaN in {col} with median = {median_val}")

    return df


# =========================
# 🧹 CLEAN TRAIN + TEST
# =========================

train_clean = clean_with_median(train_df, "TRAIN")
test_clean  = clean_with_median(test_df, "TEST")


# =========================
# 💾 SAVE OUTPUT FILES
# =========================

train_clean.to_csv("train_cleaned.csv", index=False)
test_clean.to_csv("test_cleaned.csv", index=False)

print("\n🎉 CLEANING COMPLETE!")
print("📁 Saved: train_cleaned.csv")
print("📁 Saved: test_cleaned.csv")
