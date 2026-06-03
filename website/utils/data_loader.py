from ml.feature_engineering.feature_pipeline import DATA_PATH
from website.utils.data_standardizer import (
    standardize_dataframe
)
import pandas as pd
from pathlib import Path
from website.utils.data_registry import (
    ACTIVE_DATA
)

from website.utils.ai_pipeline import (
    generate_forecast,
    generate_anomalies,
    generate_hotspots
)

# =====================================
# BUILD ANALYTICS DATA
# =====================================

def build_analytics_data():

    global ACTIVE_DATA

    # =====================================
    # RETURN ACTIVE DATA
    # =====================================

    if ACTIVE_DATA['master_df'] is not None:

        return ACTIVE_DATA

    # =====================================
    # LOAD DEFAULT FBI DATASET
    # =====================================

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_PATH = (
    BASE_DIR / "data" / "Train.csv"
)
    master_df = pd.read_csv(

        DATA_PATH,
        nrows=50000
)
    print("MASTER DF SHAPE:", master_df.shape)
    print("MASTER DF MEMORY MB:",
         round(master_df.memory_usage(deep=True).sum()/1024/1024,2))
    master_df = standardize_dataframe(
    master_df
)
    # =====================================
    # DATA CLEANING
    # =====================================

    if 'YEAR' in master_df.columns:

        master_df['YEAR'] = pd.to_numeric(

            master_df['YEAR'],

            errors='coerce'
        )

    if 'MONTH' in master_df.columns:

        master_df['MONTH'] = pd.to_numeric(

            master_df['MONTH'],

            errors='coerce'
        )

    if 'HOUR' in master_df.columns:

        master_df['HOUR'] = pd.to_numeric(

            master_df['HOUR'],

            errors='coerce'
        )

    # =====================================
    # MONTH NAME
    # =====================================

    if 'MONTH' in master_df.columns:

        master_df['Month_Name'] = pd.to_datetime(

            master_df['MONTH'],

            format='%m',

            errors='coerce'

        ).dt.strftime('%B')

    # =====================================
    # WEEKDAY
    # =====================================

    if 'DATE' in master_df.columns:

        master_df['Weekday'] = (

            pd.to_datetime(

                master_df['DATE'],

                errors='coerce'

            ).dt.day_name()
        )

    # =====================================
    # QUARTER
    # =====================================

    if 'DATE' in master_df.columns:

        master_df['Quarter'] = (

            pd.to_datetime(

                master_df['DATE'],

                errors='coerce'

            ).dt.quarter
        )

    # =====================================
    # WEEKEND FLAG
    # =====================================

    if 'Weekday' in master_df.columns:

        master_df['Weekend_Flag'] = (

            master_df['Weekday']
            .isin(['Saturday', 'Sunday'])
        )

    # =====================================
    # TIME PERIOD
    # =====================================

    def classify_time_period(hour):

        if pd.isna(hour):

            return "Unknown"

        hour = int(hour)

        if 5 <= hour < 12:

            return "Morning"

        elif 12 <= hour < 17:

            return "Afternoon"

        elif 17 <= hour < 21:

            return "Evening"

        else:

            return "Night"

    if 'HOUR' in master_df.columns:

        master_df['Time_Period'] = (

            master_df['HOUR']
            .apply(classify_time_period)
        )

    # =====================================
    # CRIME COUNT
    # =====================================

    master_df['Crime_Count'] = 1

    # =====================================
    # FORECAST ENGINE
    # =====================================

    try:

        forecast_df = generate_forecast(

            master_df
        )
        print("FORECAST DF SHAPE:", forecast_df.shape)
    except Exception as e:

        print(f"FORECAST ERROR: {e}")

        forecast_df = pd.DataFrame()

    # =====================================
    # ANOMALY ENGINE
    # =====================================

    try:

        anomaly_df = generate_anomalies(

            master_df
        )
        print("ANOMALY DF SHAPE:", anomaly_df.shape)
    except Exception as e:

        print(f"ANOMALY ERROR: {e}")

        anomaly_df = pd.DataFrame()

    # =====================================
    # HOTSPOT ENGINE
    # =====================================

    try:

        cluster_df = generate_hotspots(

            master_df
        )
        print("CLUSTER DF SHAPE:", cluster_df.shape)
    except Exception as e:

        print(f"HOTSPOT ERROR: {e}")

        cluster_df = pd.DataFrame()

    # =====================================
    # RISK DATAFRAME
    # =====================================

    try:

        if (

            not cluster_df.empty
            and
            'Cluster' in cluster_df.columns
        ):

            risk_df = (

                cluster_df
                .groupby('Cluster')
                .size()
                .reset_index(name='Crime_Count')
            )

            risk_df['Cluster_Name'] = (

                "Zone "
                +
                risk_df['Cluster'].astype(str)
            )

        else:

            risk_df = pd.DataFrame()

    except Exception as e:

        print(f"RISK ERROR: {e}")

        risk_df = pd.DataFrame()

    # =====================================
    # STORE ACTIVE DATA
    # =====================================

    ACTIVE_DATA['master_df'] = master_df

    ACTIVE_DATA['forecast_df'] = forecast_df

    ACTIVE_DATA['anomaly_df'] = anomaly_df

    ACTIVE_DATA['cluster_df'] = cluster_df

    ACTIVE_DATA['risk_df'] = risk_df

    return ACTIVE_DATA


# =====================================
# SAFE SAMPLE
# =====================================

def safe_sample(df, n=5000):

    if df.empty:

        return df

    return df.sample(

        min(n, len(df)),

        random_state=42
    )


# =====================================
# GLOBAL COLORS
# =====================================

COLORS = {

    "background": "#020617",

    "surface": "#081120",

    "card": "#0f172a",

    "card_secondary": "#111827",

    "grid": "rgba(255,255,255,0.08)",

    "border": "rgba(255,255,255,0.06)",

    "text_primary": "#ffffff",

    "text_secondary": "#e2e8f0",

    "text_muted": "#94a3b8",

    "purple": "#8b5cf6",

    "cyan": "#06b6d4",

    "green": "#22c55e",

    "red": "#ef4444",

    "orange": "#f59e0b"
}

# =====================================
# PLOT LAYOUT
# =====================================

PLOT_LAYOUT = dict(

    template="plotly_dark",

    paper_bgcolor=COLORS["background"],

    plot_bgcolor=COLORS["background"],

    font=dict(

        family="Inter, sans-serif",

        size=14,

        color=COLORS["text_primary"]
    ),

    margin=dict(

        l=60,

        r=40,

        t=70,

        b=60
    )
)

# =====================================
# AXIS STYLE
# =====================================

AXIS_STYLE = dict(

    showgrid=True,

    gridcolor=COLORS["grid"],

    zeroline=False,

    tickfont=dict(

        size=13,

        color=COLORS["text_secondary"]
    )
)

# =====================================
# LEGEND STYLE
# =====================================

LEGEND_STYLE = dict(

    bgcolor="rgba(0,0,0,0)",

    font=dict(

        size=13,

        color=COLORS["text_primary"]
    )
)

# =====================================
# MAP STYLE
# =====================================

MAPBOX_STYLE = "carto-darkmatter"

# =====================================
# TABLE STYLE
# =====================================

TABLE_CLASSES = (

    "table table-dark table-hover align-middle"
)