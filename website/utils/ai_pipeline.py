import pandas as pd
import numpy as np
from website.config import DATA_PATH
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

from website.utils.forecast_engine import (
    generate_prophet_forecast
)

from website.utils.dataset_profiler import (
    profile_dataset
)

# =====================================
# EMPTY SAFE DATAFRAMES
# =====================================

EMPTY_FORECAST = pd.DataFrame(
    columns=[
        'Date',
        'Predicted_Crime_Count'
    ]
)

EMPTY_ANOMALY = pd.DataFrame(
    columns=[
        'Date',
        'Crime_Count',
        'Anomaly_Label'
    ]
)

EMPTY_HOTSPOT = pd.DataFrame(
    columns=[
        'Latitude',
        'Longitude',
        'Cluster'
    ]
)

# =====================================
# GENERATE FORECAST
# =====================================

def generate_forecast(df):

    """
    Generate predictive forecast data.
    """

    try:

        if df is None or df.empty:

            return EMPTY_FORECAST.copy()

        profile = profile_dataset(df)

        if not profile.get('supports_forecasting', False):

            print(
                "\nFORECASTING DISABLED:"
                " Missing temporal columns.\n"
            )

            return EMPTY_FORECAST.copy()

        if 'DATE' not in df.columns:

            return EMPTY_FORECAST.copy()

        local_df = df.copy()

        local_df['DATE'] = pd.to_datetime(
            local_df['DATE'],
            errors='coerce'
        )

        local_df = local_df.dropna(
            subset=['DATE']
        )

        if local_df.empty:

            return EMPTY_FORECAST.copy()

        local_df['Crime_Count'] = 1

        trend_df = (
            local_df
            .groupby('DATE')
            .size()
            .reset_index(name='Crime_Count')
            .sort_values('DATE')
        )

        if trend_df.empty:

            return EMPTY_FORECAST.copy()

        trend_df['Predicted_Crime_Count'] = (
            trend_df['Crime_Count']
            .rolling(
                window=7,
                min_periods=1
            )
            .mean()
            .round(2)
        )

        forecast_df = trend_df.rename(
            columns={
                'DATE': 'Date'
            }
        )

        if forecast_df.empty:

            return EMPTY_FORECAST.copy()

        return forecast_df

    except Exception as e:

        print(f"\nFORECAST ERROR: {e}\n")

        return EMPTY_FORECAST.copy()

# =====================================
# GENERATE ANOMALIES
# =====================================

def generate_anomalies(df):

    try:

        if df is None or df.empty:

            return EMPTY_ANOMALY.copy()

        # =====================================
        # REQUIRED COLUMN CHECK
        # =====================================

        if 'DATE' not in df.columns:

            return EMPTY_ANOMALY.copy()

        # =====================================
        # CLEAN DATE
        # =====================================

        local_df = df.copy()

        local_df['DATE'] = pd.to_datetime(

            local_df['DATE'],

            errors='coerce'
        )

        local_df = local_df.dropna(

            subset=['DATE']
        )

        if local_df.empty:

            return EMPTY_ANOMALY.copy()

        # =====================================
        # DAILY CRIME AGGREGATION
        # =====================================

        daily_crime = (

            local_df
            .groupby('DATE')
            .size()
            .reset_index(name='Crime_Count')
        )

        # =====================================
        # MINIMUM SIZE CHECK
        # =====================================

        if len(daily_crime) < 30:

            return EMPTY_ANOMALY.copy()

        # =====================================
        # ISOLATION FOREST
        # =====================================

        model = IsolationForest(

            contamination=0.05,
            random_state=42
        )

        daily_crime['ANOMALY'] = model.fit_predict(

            daily_crime[['Crime_Count']]
        )

        # =====================================
        # LABELS
        # =====================================

        daily_crime['Anomaly_Label'] = (

            daily_crime['ANOMALY']
            .map({

                -1: 'Anomaly',
                1: 'Normal'
            })
        )
        print("\n========= ANOMALY DATA =========")
        print(daily_crime.head())
        print(daily_crime['Anomaly_Label'].value_counts())
        print("================================\n")
        return daily_crime

    except Exception as e:

        print(f"\nANOMALY ERROR: {e}\n")

        return EMPTY_ANOMALY.copy()

# =====================================
# GENERATE HOTSPOTS
# =====================================

def generate_hotspots(df):

    try:

        if df is None or df.empty:

            return EMPTY_HOTSPOT.copy()

        # =====================================
        # VALIDATE REQUIRED COLUMNS
        # =====================================

        required_columns = [

            'Latitude',
            'Longitude'
        ]

        for col in required_columns:

            if col not in df.columns:

                return EMPTY_HOTSPOT.copy()

        # =====================================
        # CLEAN COORDINATES
        # =====================================

        coords = df[[
            'Latitude',
            'Longitude'
        ]].copy()

        coords['Latitude'] = pd.to_numeric(
            coords['Latitude'],
            errors='coerce'
        )

        coords['Longitude'] = pd.to_numeric(
            coords['Longitude'],
            errors='coerce'
        )

        coords = coords.dropna()

        # =====================================
        # VALID GEO FILTER
        # =====================================

        coords = coords[
            (coords['Latitude'].between(-90, 90))
            &
            (coords['Longitude'].between(-180, 180))
        ]

        # =====================================
        # MINIMUM DATA CHECK
        # =====================================

        if len(coords) < 50:

            return EMPTY_HOTSPOT.copy()

        # =====================================
        # SAFE SAMPLING
        # =====================================

        sample_size = min(

            len(coords),
            3000
        )

        sample_df = coords.sample(

            sample_size,

            random_state=42
        )

        # =====================================
        # DBSCAN MODEL
        # =====================================

        db = DBSCAN(

            eps=0.01,
            min_samples=15,
            algorithm='ball_tree'
        )

        # =====================================
        # FIT CLUSTERS
        # =====================================

        clusters = db.fit_predict(sample_df)

        sample_df['Cluster'] = clusters

        # =====================================
        # REMOVE NOISE
        # =====================================

        sample_df = sample_df[
            sample_df['Cluster'] != -1
        ]

        # =====================================
        # EMPTY SAFETY
        # =====================================

        if sample_df.empty:

            return EMPTY_HOTSPOT.copy()

        return sample_df

    except Exception as e:

        print(f"\nHOTSPOT ERROR: {e}\n")

        return EMPTY_HOTSPOT.copy()

# =====================================
# AI CONFIDENCE SCORE
# =====================================

def calculate_ai_confidence(
    forecast_df,
    anomaly_df,
    hotspot_df
):

    try:

        score = 70

        if forecast_df is not None and not forecast_df.empty:

            score += 10

        if anomaly_df is not None and not anomaly_df.empty:

            score += 10

        if hotspot_df is not None and not hotspot_df.empty:

            score += 10

        return min(score, 99)

    except Exception:

        return 75

# =====================================
# THREAT LEVEL ENGINE
# =====================================

def calculate_threat_level(
    total_crimes,
    anomaly_count
):

    if anomaly_count >= 15:

        return 'CRITICAL'

    if anomaly_count >= 8:

        return 'HIGH'

    if total_crimes >= 500:

        return 'MODERATE'

    return 'LOW'

# =====================================
# RUN FULL AI PIPELINE
# =====================================

def run_ai_pipeline(df):

    """
    Execute complete AI pipeline.
    """

    forecast_df = generate_forecast(df)

    anomaly_df = generate_anomalies(df)

    hotspot_df = generate_hotspots(df)

    anomaly_count = 0

    if (
        anomaly_df is not None
        and
        not anomaly_df.empty
        and
        'Anomaly_Label' in anomaly_df.columns
    ):

        anomaly_count = len(
            anomaly_df[
                anomaly_df['Anomaly_Label'] == 'Anomaly'
            ]
        )

    ai_confidence = calculate_ai_confidence(
        forecast_df,
        anomaly_df,
        hotspot_df
    )

    total_crimes = (
        len(df)
        if df is not None
        else 0
    )

    threat_level = calculate_threat_level(
        total_crimes,
        anomaly_count
    )

    return {

        'forecast_df': forecast_df,

        'anomaly_df': anomaly_df,

        'cluster_df': hotspot_df,

        'ai_confidence': ai_confidence,

        'threat_level': threat_level,

        'anomaly_count': anomaly_count
    }