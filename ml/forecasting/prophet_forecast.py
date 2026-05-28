import pandas as pd

from prophet import Prophet

from pathlib import Path

import joblib

import numpy as np

# =========================================
# PROJECT PATHS
# =========================================

BASE_DIR = Path("D:/FBI_Crime_Project")

FEATURE_PATH = (
    BASE_DIR /
    "ml" /
    "outputs" /
    "engineered_features.csv"
)

FORECAST_OUTPUT = (
    BASE_DIR /
    "ml" /
    "outputs" /
    "future_forecast.csv"
)

MODEL_OUTPUT = (
    BASE_DIR /
    "ml" /
    "models" /
    "prophet_model.pkl"
)

# =========================================
# LOAD ENGINEERED FEATURES
# =========================================

df = pd.read_csv(FEATURE_PATH)

print("\nENGINEERED FEATURES LOADED\n")

# =========================================
# PREPARE DATA
# =========================================

prophet_df = df[['DATE', 'CRIME_COUNT']].copy()

prophet_df.columns = ['ds', 'y']

prophet_df['ds'] = pd.to_datetime(
    prophet_df['ds']
)

# =========================================
# INITIALIZE PROPHET MODEL
# =========================================

model = Prophet(

    yearly_seasonality=True,

    weekly_seasonality=False,

    daily_seasonality=False,

    changepoint_prior_scale=0.15,

    seasonality_prior_scale=10,

    interval_width=0.95
)

# =========================================
# TRAIN MODEL
# =========================================

print("\nTRAINING PROPHET MODEL...\n")

model.fit(prophet_df)

print("\nMODEL TRAINING COMPLETE\n")

# =========================================
# CREATE FUTURE TIMELINE
# =========================================

future = model.make_future_dataframe(

    periods=24,

    freq='ME'
)

# =========================================
# GENERATE FORECAST
# =========================================

forecast = model.predict(future)

# =========================================
# CLEAN FORECAST
# =========================================

forecast_output = forecast[[

    'ds',

    'yhat',

    'yhat_lower',

    'yhat_upper',

    'trend',

    'trend_lower',

    'trend_upper'

]].copy()

# =========================================
# RENAME COLUMNS
# =========================================

forecast_output.columns = [

    'Date',

    'Predicted_Crime_Count',

    'Lower_Bound',

    'Upper_Bound',

    'Trend',

    'Trend_Lower',

    'Trend_Upper'
]

# =========================================
# EXTRACT DATE COMPONENTS
# =========================================

forecast_output['YEAR'] = (
    forecast_output['Date']
    .dt.year
)

forecast_output['MONTH'] = (
    forecast_output['Date']
    .dt.month
)

# =========================================
# FORECAST VOLATILITY
# =========================================

forecast_output['Forecast_Range'] = (

    forecast_output['Upper_Bound']
    -
    forecast_output['Lower_Bound']
)

forecast_output['Volatility_Index'] = (

    forecast_output['Forecast_Range']
    /
    forecast_output['Predicted_Crime_Count']
)

# =========================================
# THREAT CLASSIFICATION
# =========================================

high_threshold = (
    forecast_output['Predicted_Crime_Count']
    .quantile(0.80)
)

medium_threshold = (
    forecast_output['Predicted_Crime_Count']
    .quantile(0.50)
)

def classify_threat(value):

    if value >= high_threshold:

        return "HIGH"

    elif value >= medium_threshold:

        return "MEDIUM"

    else:

        return "LOW"

forecast_output['Forecast_Threat_Level'] = (

    forecast_output['Predicted_Crime_Count']
    .apply(classify_threat)
)

# =========================================
# RISK SCORE
# =========================================

forecast_output['Forecast_Risk_Score'] = (

    (
        forecast_output['Predicted_Crime_Count']
        /
        forecast_output['Predicted_Crime_Count'].max()
    )
    * 100
).round(2)

# =========================================
# ROUND NUMERIC VALUES
# =========================================

numeric_cols = [

    'Predicted_Crime_Count',

    'Lower_Bound',

    'Upper_Bound',

    'Trend',

    'Trend_Lower',

    'Trend_Upper',

    'Forecast_Range',

    'Volatility_Index',

    'Forecast_Risk_Score'
]

forecast_output[numeric_cols] = (

    forecast_output[numeric_cols]
    .round(2)
)

# =========================================
# SAVE FORECAST
# =========================================

forecast_output.to_csv(

    FORECAST_OUTPUT,

    index=False
)

# =========================================
# SAVE MODEL
# =========================================

joblib.dump(

    model,

    MODEL_OUTPUT
)

# =========================================
# OUTPUT SUMMARY
# =========================================

print("\nFORECAST GENERATED SUCCESSFULLY\n")

print(

    forecast_output[[

        'Date',

        'Predicted_Crime_Count',

        'Forecast_Threat_Level',

        'Forecast_Risk_Score'

    ]].tail()

)

print("\nFORECAST SAVED TO:\n")

print(FORECAST_OUTPUT)

print("\nMODEL SAVED TO:\n")

print(MODEL_OUTPUT)

print("\nFORECASTING PIPELINE COMPLETE\n")