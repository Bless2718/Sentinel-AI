import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np

# =========================================
# LOAD DATA
# =========================================

forecast_df = pd.read_csv(
    "D:/FBI_Crime_Project/ml/outputs/future_forecast.csv"
)

master_df = pd.read_csv(
    "D:/FBI_Crime_Project/data/final_cleaned_crime_data.csv"
)

# =========================================
# PREPARE ACTUAL DATA
# =========================================

actual = (

    master_df
    .groupby(['YEAR', 'MONTH'])
    .size()
    .reset_index(name='CRIME_COUNT')
)

actual['DATE'] = pd.to_datetime(

    dict(
        year=actual['YEAR'],
        month=actual['MONTH'],
        day=1
    )
)

# =========================================
# PREPARE FORECAST DATA
# =========================================

forecast_df['ds'] = pd.to_datetime(
    forecast_df['ds']
)

forecast_df = forecast_df.rename(
    columns={
        'ds': 'DATE',
        'yhat': 'PREDICTED'
    }
)

# =========================================
# MERGE
# =========================================

merged = pd.merge(

    actual,

    forecast_df,

    on='DATE',

    how='inner'
)

# =========================================
# EVALUATION
# =========================================

y_true = merged['CRIME_COUNT']

y_pred = merged['PREDICTED']

mae = mean_absolute_error(
    y_true,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_true,
        y_pred
    )
)

r2 = r2_score(
    y_true,
    y_pred
)

mape = np.mean(

    np.abs(
        (y_true - y_pred) / y_true
    )

) * 100

# =========================================
# RESULTS
# =========================================

print("\nMODEL EVALUATION RESULTS\n")

print(f"MAE  : {mae:.2f}")

print(f"RMSE : {rmse:.2f}")

print(f"R²   : {r2:.4f}")

print(f"MAPE : {mape:.2f}%")

# =========================================
# SAVE RESULTS
# =========================================

results = pd.DataFrame({

    "Metric": [
        "MAE",
        "RMSE",
        "R2",
        "MAPE"
    ],

    "Value": [
        mae,
        rmse,
        r2,
        mape
    ]
})

results.to_csv(

    "D:/FBI_Crime_Project/ml/outputs/model_metrics.csv",

    index=False
)

print("\nMETRICS SAVED SUCCESSFULLY")