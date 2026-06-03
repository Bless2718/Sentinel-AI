import pandas as pd

import numpy as np

import joblib

from pathlib import Path

from sklearn.ensemble import IsolationForest

from sklearn.preprocessing import MinMaxScaler

# =========================================
# PROJECT PATHS
# =========================================

BASE_DIR = Path("(__file__).resolve().parents[2]")

FEATURE_PATH = (
    BASE_DIR /
    "ml" /
    "outputs" /
    "engineered_features.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "ml" /
    "outputs" /
    "crime_anomalies_detected.csv"
)

MODEL_PATH = (
    BASE_DIR /
    "ml" /
    "models" /
    "isolation_forest_model.pkl"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(FEATURE_PATH)

print("\nENGINEERED FEATURES LOADED\n")

# =========================================
# DATE PROCESSING
# =========================================

df['DATE'] = pd.to_datetime(
    df['DATE']
)

# =========================================
# SELECT FEATURES
# =========================================

features = [

    'CRIME_COUNT',

    'ROLLING_MEAN_3',

    'ROLLING_STD_3',

    'LAG_1',

    'LAG_2',

    'LAG_3',

    'VOLATILITY'
]

X = df[features].copy()

# =========================================
# HANDLE NULLS
# =========================================

X = X.fillna(0)

# =========================================
# INITIALIZE MODEL
# =========================================

print("TRAINING ANOMALY DETECTION MODEL...\n")

model = IsolationForest(

    n_estimators=400,

    contamination=0.05,

    max_samples='auto',

    random_state=42
)

# =========================================
# TRAIN MODEL
# =========================================

raw_predictions = model.fit_predict(X)

# =========================================
# CONVERT LABELS
# =========================================

df['ANOMALY'] = np.where(

    raw_predictions == -1,

    1,

    0
)

# =========================================
# ANOMALY SCORE
# =========================================

df['ANOMALY_SCORE'] = (

    model.decision_function(X)
)

# =========================================
# NORMALIZE RISK SCORE
# =========================================

risk_scaler = MinMaxScaler(

    feature_range=(0, 100)
)

df['RISK_SCORE'] = risk_scaler.fit_transform(

    (-df[['ANOMALY_SCORE']])
)

df['RISK_SCORE'] = (

    df['RISK_SCORE']
    .round(2)
)

# =========================================
# THREAT LEVELS
# =========================================

def classify_threat(score):

    if score >= 75:

        return "CRITICAL"

    elif score >= 55:

        return "HIGH"

    elif score >= 35:

        return "MEDIUM"

    else:

        return "LOW"

df['THREAT_LEVEL'] = (

    df['RISK_SCORE']
    .apply(classify_threat)
)

# =========================================
# HUMAN READABLE LABELS
# =========================================

df['Anomaly_Label'] = np.where(

    df['ANOMALY'] == 1,

    "Anomaly",

    "Normal"
)

# =========================================
# CONFIDENCE SCORE
# =========================================

df['CONFIDENCE_SCORE'] = (

    100 - df['RISK_SCORE']
).round(2)

# =========================================
# TEMPORAL INTELLIGENCE
# =========================================

df['YEAR'] = (

    df['DATE']
    .dt.year
)

df['MONTH'] = (

    df['DATE']
    .dt.month
)

df['QUARTER'] = (

    df['DATE']
    .dt.quarter
)

# =========================================
# ANOMALY SUMMARY
# =========================================

total_anomalies = int(

    df['ANOMALY'].sum()
)

print(f"TOTAL ANOMALIES DETECTED: {total_anomalies}")

print("\nANOMALY SAMPLE:\n")

print(

    df[

        df['ANOMALY'] == 1

    ][[

        'DATE',

        'CRIME_COUNT',

        'RISK_SCORE',

        'THREAT_LEVEL',

        'ANOMALY_SCORE'

    ]].head()

)

# =========================================
# SAVE RESULTS
# =========================================

df.to_csv(

    OUTPUT_PATH,

    index=False
)

# =========================================
# SAVE MODEL
# =========================================

joblib.dump(

    model,

    MODEL_PATH
)

# =========================================
# COMPLETION MESSAGE
# =========================================

print("\nANOMALY DATA SAVED:\n")

print(OUTPUT_PATH)

print("\nMODEL SAVED:\n")

print(MODEL_PATH)

print("\nANOMALY INTELLIGENCE PIPELINE COMPLETE\n")