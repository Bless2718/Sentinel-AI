import pandas as pd
from website.utils.severity_engine import (
    calculate_dataframe_severity
)
# =====================================
# CRIME SEVERITY MAP
# =====================================



# =====================================
# CALCULATE RISK ENGINE
# =====================================

def calculate_risk_engine(

    master_df,
    anomaly_df,
    forecast_df,
    hotspot_df
):

    # =====================================
    # DEFAULT RESPONSE
    # =====================================

    response = {

        "risk_score": 0,

        "threat_level": "LOW",

        "risk_color": "#22c55e"
    }

    # =====================================
    # EMPTY SAFETY
    # =====================================

    if master_df.empty:

        return response

    # =====================================
    # BASE SCORE
    # =====================================

    risk_score = 0

    # =====================================
    # CRIME SEVERITY
    # =====================================

    severity_score = calculate_dataframe_severity(

        master_df
    )

    risk_score += min(

        severity_score / 10,

        30
    )

    # =====================================
    # ANOMALY SCORE
    # =====================================

    anomaly_count = 0

    if 'ANOMALY' in anomaly_df.columns:

        anomaly_count = len(

            anomaly_df[
                anomaly_df['ANOMALY'] == -1
            ]
        )

    risk_score += min(

        anomaly_count * 2,

        25
    )

    # =====================================
    # FORECAST ESCALATION
    # =====================================

    if (

        not forecast_df.empty
        and
        'Predicted_Crime_Count'
        in forecast_df.columns
    ):

        first_value = forecast_df[
            'Predicted_Crime_Count'
        ].iloc[0]

        latest_value = forecast_df[
            'Predicted_Crime_Count'
        ].iloc[-1]

        if latest_value > first_value:

            growth = latest_value - first_value

            risk_score += min(

                growth,

                20
            )

    # =====================================
    # HOTSPOT DENSITY
    # =====================================

    hotspot_count = 0

    if 'Cluster' in hotspot_df.columns:

        hotspot_count = hotspot_df[
            'Cluster'
        ].nunique()

    risk_score += min(

        hotspot_count * 2,

        15
    )

    # =====================================
    # TREND GROWTH
    # =====================================

    if 'YEAR' in master_df.columns:

        yearly = (

            master_df
            .groupby('YEAR')
            .size()
            .reset_index(name='COUNT')
        )

        if len(yearly) > 1:

            first_year = yearly[
                'COUNT'
            ].iloc[0]

            latest_year = yearly[
                'COUNT'
            ].iloc[-1]

            if latest_year > first_year:

                risk_score += 10

    # =====================================
    # NORMALIZE SCORE
    # =====================================

    risk_score = round(

        min(risk_score, 100),

        2
    )

    # =====================================
    # THREAT LEVEL
    # =====================================

    if risk_score >= 80:

        threat_level = "CRITICAL"

        risk_color = "#ef4444"

    elif risk_score >= 60:

        threat_level = "HIGH"

        risk_color = "#f97316"

    elif risk_score >= 40:

        threat_level = "MODERATE"

        risk_color = "#eab308"

    else:

        threat_level = "LOW"

        risk_color = "#22c55e"

    # =====================================
    # FINAL RESPONSE
    # =====================================

    response = {

        "risk_score": risk_score,

        "threat_level": threat_level,

        "risk_color": risk_color
    }

    return response