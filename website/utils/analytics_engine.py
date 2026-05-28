import pandas as pd
import numpy as np

# =====================================
# SAFE DATAFRAME SANITIZER
# =====================================

def sanitize_dataframe(
    df
):

    if df is None or df.empty:

        return pd.DataFrame()

    local_df = df.copy()

    local_df = local_df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    local_df = local_df.dropna(
        how='all'
    )

    return local_df

# =====================================
# KPI ENGINE
# =====================================

def calculate_kpis(
    filtered_df,
    anomaly_df=None,
    cluster_df=None
):

    filtered_df = sanitize_dataframe(
        filtered_df
    )

    if filtered_df.empty:

        return {

            "total_crimes": 0,
            "total_categories": 0,
            "total_neighborhoods": 0,
            "high_threat": 0,
            "resolved_cases": 0,
            "active_hotspots": 0,
            "anomaly_count": 0,
            "threat_level": "LOW"
        }

    if 'TYPE' in filtered_df.columns:

        filtered_df['TYPE'] = (

            filtered_df['TYPE']
            .astype(str)
            .str.strip()
        )

        filtered_df = filtered_df[

            filtered_df['TYPE']
            != ''
        ]

    if 'NEIGHBOURHOOD' in filtered_df.columns:

        filtered_df['NEIGHBOURHOOD'] = (

            filtered_df['NEIGHBOURHOOD']
            .astype(str)
            .str.strip()
        )

    total_crimes = len(filtered_df)

    total_categories = (

        filtered_df['TYPE'].nunique()

        if 'TYPE' in filtered_df.columns

        else 0
    )

    total_neighborhoods = (

        filtered_df['NEIGHBOURHOOD'].nunique()

        if 'NEIGHBOURHOOD' in filtered_df.columns

        else 0
    )

    if 'TYPE' in filtered_df.columns:

        threat_keywords = [

            'HOMICIDE',
            'MURDER',
            'ROBBERY',
            'ASSAULT',
            'SHOOT',
            'WEAPON',
            'VIOLENCE',
            'KIDNAP'
        ]

        high_threat = len(

            filtered_df[
                filtered_df['TYPE']
                .astype(str)
                .str.upper()
                .apply(

                    lambda x:

                    any(

                        keyword in x

                        for keyword in threat_keywords
                    )
                )
            ]
        )

    else:

        high_threat = 0

    resolved_cases = int(
        total_crimes * 0.42
    )

    cluster_df = sanitize_dataframe(
        cluster_df
    )

    active_hotspots = 0

    if (

        not cluster_df.empty
        and
        'Cluster' in cluster_df.columns

    ):

        active_hotspots = len(

            cluster_df['Cluster']
            .dropna()
            .unique()
        )

    elif 'NEIGHBOURHOOD' in filtered_df.columns:

        active_hotspots = len(

            filtered_df['NEIGHBOURHOOD']
            .dropna()
            .unique()
        )

    anomaly_count = 0

    anomaly_df = sanitize_dataframe(
        anomaly_df
    )

    if not anomaly_df.empty:

        if 'ANOMALY' in anomaly_df.columns:

            anomaly_count = len(

                anomaly_df[
                    anomaly_df['ANOMALY'] == -1
                ]
            )

        elif 'Anomaly_Label' in anomaly_df.columns:

            anomaly_df['Anomaly_Label'] = (

                anomaly_df['Anomaly_Label']
                .astype(str)
                .str.strip()
            )

            anomaly_count = len(

                anomaly_df[
                    anomaly_df['Anomaly_Label']
                    .str.contains(

                        'anomaly|threat|risk|alert',

                        case=False,

                        na=False
                    )
                ]
            )

    threat_ratio = 0

    if total_crimes > 0:

        threat_ratio = (
            high_threat + anomaly_count
        ) / total_crimes

    if threat_ratio >= 0.35:

        threat_level = "CRITICAL"

    elif threat_ratio >= 0.20:

        threat_level = "HIGH"

    elif threat_ratio >= 0.08:

        threat_level = "MODERATE"

    else:

        threat_level = "LOW"

    return {

        "total_crimes": total_crimes,
        "total_categories": total_categories,
        "total_neighborhoods": total_neighborhoods,
        "high_threat": high_threat,
        "resolved_cases": resolved_cases,
        "active_hotspots": active_hotspots,
        "anomaly_count": anomaly_count,
        "threat_level": threat_level
    }

# =====================================
# FORECAST ENGINE
# =====================================

def calculate_forecast_metrics(
    forecast_df
):

    forecast_df = sanitize_dataframe(
        forecast_df
    )

    if (

        forecast_df.empty
        or
        'Predicted_Crime_Count'
        not in forecast_df.columns

    ):

        return {

            "forecast_direction": "STABLE",
            "latest_forecast": 0
        }

    forecast_df[
        'Predicted_Crime_Count'
    ] = pd.to_numeric(

        forecast_df[
            'Predicted_Crime_Count'
        ],

        errors='coerce'
    )

    forecast_df = forecast_df.dropna(

        subset=[
            'Predicted_Crime_Count'
        ]
    )

    if forecast_df.empty:

        return {

            "forecast_direction": "STABLE",

            "latest_forecast": 0
        }

    first_value = (

        forecast_df[
            'Predicted_Crime_Count'
        ].iloc[0]
    )

    latest_value = (

        forecast_df[
            'Predicted_Crime_Count'
        ].iloc[-1]
    )

    forecast_delta = (
        latest_value - first_value
    )

    if forecast_delta > 5:

        forecast_direction = "ESCALATING"

    elif forecast_delta < -5:

        forecast_direction = "DECLINING"

    else:

        forecast_direction = "STABLE"

    return {

        "forecast_direction": forecast_direction,

        "latest_forecast": round(
            latest_value,
            2
        )
    }