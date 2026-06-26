import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# =====================================================
# LOAD DATA
# =====================================================

train = pd.read_csv("train_final.csv")
test = pd.read_csv("test_final.csv")

print("Train Shape:", train.shape)
print("Test Shape :", test.shape)

# =====================================================
# FEATURES
# =====================================================

ignore_cols = [
    "Latitude",
    "Longitude",
    "Flood_Score",
    "Flood_Index"
]

feature_cols = [c for c in train.columns if c not in ignore_cols]

print("\nFeatures used:")
print(feature_cols)

X = train[feature_cols]
y = train["Flood_Score"]

# =====================================================
# TRAIN / VALIDATION SPLIT
# =====================================================

X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# =====================================================
# RANDOM FOREST MODEL
# =====================================================

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =====================================================
# VALIDATION
# =====================================================

pred = model.predict(X_valid)

print("\n====================================")
print("VALIDATION RESULTS")
print("====================================")

print("Accuracy :", accuracy_score(y_valid, pred))

print("\nClassification Report")
print(classification_report(y_valid, pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_valid, pred))

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

importance = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n====================================")
print("FEATURE IMPORTANCE")
print("====================================")

print(importance)

# =====================================================
# TRAIN ON FULL DATASET
# =====================================================

model.fit(X, y)

# =====================================================
# PREDICT TEST SET
# =====================================================

X_test = test[feature_cols]

test["Predicted_Flood_Score"] = model.predict(X_test)

# Optional probabilities
prob = model.predict_proba(X_test)

test["Prob_0"] = prob[:,0]
test["Prob_1"] = prob[:,1]
test["Prob_2"] = prob[:,2]
test["Prob_3"] = prob[:,3]

# =====================================================
# SAVE RESULTS
# =====================================================

test.to_csv(
    "Flood_Predictions.csv",
    index=False
)

joblib.dump(
    model,
    "Flood_Model.pkl"
)

print("\n====================================")
print("SUCCESS")
print("====================================")

print("Predictions saved to:")
print("Flood_Predictions.csv")

print("\nModel saved as:")
print("Flood_Model.pkl")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# LOAD DATA
# =========================================================

train = pd.read_csv("train_final.csv")
test = pd.read_csv("Flood_Predictions.csv")

# =========================================================
# 1. FLOOD SUSCEPTIBILITY MAP (TEST DATA)
# =========================================================

plt.figure(figsize=(10,7))

scatter = plt.scatter(
    test["Longitude"],
    test["Latitude"],
    c=test["Predicted_Flood_Score"],
    cmap="RdYlGn_r",
    s=15,
    alpha=0.8
)

plt.colorbar(scatter, label="Flood Score (Predicted)")
plt.title("Flood Susceptibility Map (Karnataka)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, alpha=0.3)
plt.show()


# =========================================================
# 2. FLOOD SCORE DISTRIBUTION (TRAIN vs TEST)
# =========================================================

plt.figure(figsize=(8,5))

train_counts = train["Flood_Score"].value_counts().sort_index()
test_counts = test["Predicted_Flood_Score"].value_counts().sort_index()

classes = [0,1,2,3]

plt.bar(np.array(classes)-0.2,
        train_counts.reindex(classes, fill_value=0),
        width=0.4,
        label="Train")

plt.bar(np.array(classes)+0.2,
        test_counts.reindex(classes, fill_value=0),
        width=0.4,
        label="Test")

plt.xticks(classes)
plt.xlabel("Flood Score")
plt.ylabel("Count")
plt.title("Flood Score Distribution (Train vs Test)")
plt.legend()
plt.show()


# =========================================================
# 3. FEATURE IMPORTANCE (Random Forest)
# =========================================================

importance = pd.DataFrame({
    "Feature": X_valid.columns,
    "Importance": model.feature_importances_
}).sort_values("Importance")

plt.figure(figsize=(8,6))
plt.barh(importance["Feature"], importance["Importance"])
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance")
plt.show()


# =========================================================
# 4. CORRELATION HEATMAP
# =========================================================

plt.figure(figsize=(10,8))
sns.heatmap(train.corr(numeric_only=True), cmap="coolwarm", annot=False)
plt.title("Feature Correlation Heatmap")
plt.show()


# =========================================================
# 5. RAINFALL vs FLOOD SCORE
# =========================================================

plt.figure(figsize=(8,5))
sns.boxplot(x="Flood_Score", y="rainfall", data=train)
plt.title("Rainfall vs Flood Score")
plt.show()


# =========================================================
# 6. ELEVATION vs FLOOD SCORE
# =========================================================

plt.figure(figsize=(8,5))
sns.boxplot(x="Flood_Score", y="Elevation", data=train)
plt.title("Elevation vs Flood Score")
plt.show()


# =========================================================
# 7. RIVER DISTANCE vs FLOOD SCORE
# =========================================================

plt.figure(figsize=(8,5))
sns.boxplot(x="Flood_Score", y="river_distance", data=train)
plt.title("River Distance vs Flood Score")
plt.show()


# =========================================================
# 8. CONFUSION MATRIX
# =========================================================

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_predictions(y_valid, pred, cmap="Blues")
plt.title("Confusion Matrix")
plt.show()


# =========================================================
# 9. ACTUAL vs PREDICTED (VALIDATION SET)
# =========================================================

plt.figure(figsize=(6,6))

plt.scatter(y_valid, pred, alpha=0.6)

plt.plot([0,3],[0,3],'r--')

plt.xlabel("Actual Flood Score")
plt.ylabel("Predicted Flood Score")
plt.title("Actual vs Predicted Flood Score")
plt.xticks([0,1,2,3])
plt.yticks([0,1,2,3])
plt.grid()
plt.show()
