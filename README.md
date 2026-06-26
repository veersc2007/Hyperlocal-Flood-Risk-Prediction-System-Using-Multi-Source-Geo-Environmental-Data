# 🌊 Hyperlocal Flood Risk Prediction System Using Multi-Source Geo-Environmental Data

## 📌 Project Overview

This project presents a **machine learning-based hyperlocal flood risk prediction system** developed using multi-source geo-environmental datasets.

The system integrates **satellite, terrain, soil, and hydrological data** to predict flood risk intensity on a **0–3 scale (low to high risk)** at a high spatial resolution over selected regions of Karnataka, India.

The final output includes **flood susceptibility maps, statistical analysis, and geospatial visualizations** for decision-making and disaster risk assessment.

---

## 🎯 Objective

- Integrate heterogeneous geospatial datasets from multiple global and local sources
- Preprocess and align spatial data into a unified ML-ready format
- Train a supervised machine learning model to classify flood risk (0–3 scale)
- Generate predictive flood risk maps for unseen regions
- Analyze environmental influence on flooding behavior

---

## 🗺️ Study Area

- Two regions in Karnataka, India
- One region used for training
- One region used for testing (proxy validation area)

---

## 📊 Datasets Used

The project integrates **five major data sources**:

### 1. 🌍 NASA Earth Observation Data
- Satellite-based environmental variables
- Used for rainfall and atmospheric conditions

**Source:** NASA Earthdata  
https://earthdata.nasa.gov/

---

### 2. 🏔️ Digital Elevation Model (DEM)
- Derived using QGIS / SRTM-based elevation data
- Used for terrain and altitude influence on flooding

**Source:** NASA SRTM / QGIS Processing Tools  
https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm

---

### 3. 📉 Slope Dataset (Derived from DEM using QGIS)
- Calculated terrain slope
- Used to determine runoff behavior and water accumulation zones

**Source Tool:** QGIS  
https://qgis.org/

---

### 4. 🌱 Soil Properties Dataset
- Soil composition features:
  - Sand content
  - Silt content
  - Clay content
- Used to estimate infiltration and water retention capacity

**Source:** ISRIC SoilGrids  
https://soilgrids.org/

---

### 5. 🌧️ Rainfall Dataset
- Historical rainfall data
- Preprocessed and split for training/testing regions

**Source:** NASA / ERA5 / Meteorological datasets  
https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5

---

## 🧠 Methodology

### 1. Data Preprocessing
- Conversion of raster datasets into tabular CSV format
- Handling missing values and inconsistencies
- Spatial alignment using latitude-longitude grids

### 2. Feature Engineering
- Integration of:
  - rainfall
  - elevation
  - slope
  - soil properties
  - hydrological proximity features
- Normalization and scaling

### 3. Dataset Preparation
- Training dataset (Region 1 - Karnataka)
- Testing dataset (Region 2 - Karnataka)
- Target variable: **Flood Risk Score (0–3)**

---

## 🤖 Machine Learning Model

- Model Used: Random Forest Regressor / Classifier
- Input: Geo-environmental features
- Output: Flood risk score (0–3 scale)

### Training Process:
- Train-test split on Region 1 data
- Validation on Region 2 (proxy real-world testing)

---

## 📈 Model Evaluation

- Confusion Matrix (classification performance)
- Feature Importance Analysis

---

## 🗺️ Visual Outputs Generated

- 🌊 Flood Risk Heatmaps (lat-long grid)
- 📍 Flood Risk Map of Karnataka
- 📊 Flood Score vs Elevation plots
- 🌊 Flood Score vs River Distance plots
- 📉 Correlation Heatmaps
- 📊 Confusion Matrix visualization

---

## 🔍 Key Insights

- Elevation and slope strongly influence flood susceptibility
- Areas near river networks show higher flood risk
- Soil composition significantly affects water retention behavior
- Model successfully captures spatial flood risk variation

---

## 🛠️ Tech Stack

- Python 🐍
- Pandas, NumPy
- Scikit-learn 🤖
- Xarray (for geospatial datasets)
- Matplotlib, Seaborn 📊
- QGIS (for spatial processing)
- RandomForest (machine-learning backend)

---

## 📁 Project Structure

- 
