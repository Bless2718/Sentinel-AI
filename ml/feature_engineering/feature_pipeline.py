import pandas as pd
import numpy as np
from pathlib import Path

# =========================================
# PROJECT PATHS
# =========================================

BASE_DIR = Path("D:/FBI_Crime_Project")

DATA_PATH = (
    BASE_DIR /
    "data" /
    "final_cleaned_crime_data.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "ml" /
    "outputs" /
    "engineered_features.csv"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(DATA_PATH)

print("\nDATASET LOADED\n")

# =========================================
# CREATE DATE COLUMN
# =========================================

df['DATE'] = pd.to_datetime(

    dict(
        year=df['YEAR'],
        month=df['MONTH'],
        day=1
    ),

    errors='coerce'
)

# =========================================
# REMOVE INVALID DATES
# =========================================

df.dropna(subset=['DATE'], inplace=True)

# =========================================
# TEMPORAL FEATURES
# =========================================

df['QUARTER'] = (

    df['DATE']
    .dt
    .quarter
)

df['MONTH_SIN'] = np.sin(

    2 * np.pi * df['MONTH'] / 12
)

df['MONTH_COS'] = np.cos(

    2 * np.pi * df['MONTH'] / 12
)

# =========================================
# MONTHLY AGGREGATION
# =========================================

monthly_crime = (

    df
    .groupby('DATE')
    .size()
    .reset_index(name='CRIME_COUNT')
)

# =========================================
# ROLLING MEAN
# =========================================

monthly_crime['ROLLING_MEAN_3'] = (

    monthly_crime['CRIME_COUNT']
    .rolling(window=3)
    .mean()
)

# =========================================
# ROLLING STD
# =========================================

monthly_crime['ROLLING_STD_3'] = (

    monthly_crime['CRIME_COUNT']
    .rolling(window=3)
    .std()
)

# =========================================
# GROWTH RATE
# =========================================

monthly_crime['GROWTH_RATE'] = (

    monthly_crime['CRIME_COUNT']
    .pct_change()
)

# =========================================
# LAG FEATURES
# =========================================

monthly_crime['LAG_1'] = (

    monthly_crime['CRIME_COUNT']
    .shift(1)
)

monthly_crime['LAG_2'] = (

    monthly_crime['CRIME_COUNT']
    .shift(2)
)

monthly_crime['LAG_3'] = (

    monthly_crime['CRIME_COUNT']
    .shift(3)
)

# =========================================
# VOLATILITY FEATURE
# =========================================

monthly_crime['VOLATILITY'] = (

    monthly_crime['ROLLING_STD_3'] /

    monthly_crime['ROLLING_MEAN_3']
)

# =========================================
# DROP NULLS
# =========================================

monthly_crime.dropna(inplace=True)

# =========================================
# SAVE ENGINEERED FEATURES
# =========================================

monthly_crime.to_csv(

    OUTPUT_PATH,

    index=False
)

# =========================================
# SUCCESS MESSAGE
# =========================================

print("\nFEATURE ENGINEERING COMPLETE\n")

print(monthly_crime.head())

print("\nFEATURES SAVED TO:\n")

print(OUTPUT_PATH)