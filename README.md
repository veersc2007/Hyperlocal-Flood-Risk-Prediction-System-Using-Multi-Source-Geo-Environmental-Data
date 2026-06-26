# 🌊 Hyperlocal Flood Risk Prediction System Using Multi-Source Geo-Environmental Data

## 📌 Project Overview

This project develops a **machine learning-based hyperlocal flood risk prediction system** using multi-source geo-environmental data such as rainfall, temperature, elevation, river proximity, and other terrain and climate variables.

The system predicts **flood risk at fine spatial resolution**, helping improve early warning systems, disaster preparedness, and infrastructure planning.

---

## 🎯 Objectives

- Collect and integrate multi-source geospatial datasets (ERA5, DEM, hydrological data, etc.)
- Preprocess and align spatial-temporal data for machine learning
- Build predictive models for flood risk estimation
- Generate **flood susceptibility maps**
- Identify key environmental drivers using feature importance analysis

---

## 🧠 Methodology

### 1. Data Collection
- ERA5 climate reanalysis dataset (rainfall, temperature, pressure, etc.)
- Digital Elevation Model (DEM)
- Hydrological features (river distance, slope, etc.)

### 2. Data Preprocessing
- Handling missing values
- Spatial alignment (latitude-longitude grid standardization)
- Temporal aggregation (daily/monthly conversion)

### 3. Feature Engineering
- Normalization and scaling
- Correlation analysis
- Derived environmental indicators

### 4. Model Development
- Random Forest Regressor / Classifier
- Train-validation-test split
- Hyperparameter tuning

### 5. Evaluation
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- R² Score
- Confusion Matrix (for classification models)

### 6. Visualization
- Flood risk heatmaps
- Feature importance plots
- Correlation heatmaps

---

## 📊 Model Performance

| Metric | Value |
|--------|------|
| MAE    | *Add value here* |
| RMSE   | *Add value here* |
| R²     | *Add value here* |

---

## 🛠️ Tech Stack

- Python 🐍
- Pandas, NumPy
- Scikit-learn 🤖
- Xarray (for ERA5 processing)
- Matplotlib, Seaborn 📊
- GeoPandas (optional GIS support)

---

## 📁 Project Structure
- Training datasets
  - soil_train.csv
  - train_with_river.csv
  - train_final.csv
  - nasa_train_dataset.csv
  - karnataka_train_with_slope.csv
  - karnataka_train_with_elevation.csv
  - karnataka_train_grid.csv
  - Merge_train_datasets.csv
- Testing datasets
  - soil_test.csv
  - test_with_river.csv
  - test_final.csv
  - nasa_test_dataset.csv
  - karnataka_test_with_slope.csv
  - karnataka_test_with_elevation.csv
  - karnataka_test_grid.csv
  - Merge_test_datasets.csv
- Important Python Scripts
  - Elevation_data_extraction.py
  - Final_Machine_Testing_and_Predictions_Mapping.py
  - Grid_definition_for_train_and_test_area.py
  - Landcover_Extraction.py
  - Merge_test_datasets.py
  - Merge_train_datasets.py
  - River_extraction.py
  - Slope_data_extraction.py
  - flood_score_generation_train.py
  - NASA_POWER_DatatoCSV.py


---

## 🌧️ Applications

- Flood early warning systems
- Urban infrastructure planning
- Disaster risk assessment
- Climate change impact studies

---

## 👨‍💻 Author

**Adityaveer Singh Chauhan**  
Civil Engineering, IIT Roorkee  

---

## ⭐ Acknowledgements

- NASA POWER Datasets
- Open-source GIS & ML libraries
- Scikit-learn community
