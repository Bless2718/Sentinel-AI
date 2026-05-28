import pandas as pd

# =====================================
# THREAT SCORE ENGINE
# =====================================

def calculate_threat_score(

    total_crimes,
    high_threat,
    anomaly_count,
    active_hotspots
):

    score = 0

    # =====================================
    # CRIME VOLUME
    # =====================================

    if total_crimes >= 10000:

        score += 35

    elif total_crimes >= 5000:

        score += 25

    elif total_crimes >= 1000:

        score += 15

    else:

        score += 5

    # =====================================
    # HIGH THREAT INCIDENTS
    # =====================================

    if high_threat >= 100:

        score += 30

    elif high_threat >= 50:

        score += 20

    elif high_threat >= 10:

        score += 10

    # =====================================
    # ANOMALIES
    # =====================================

    if anomaly_count >= 25:

        score += 20

    elif anomaly_count >= 10:

        score += 15

    elif anomaly_count >= 5:

        score += 10

    # =====================================
    # HOTSPOTS
    # =====================================

    if active_hotspots >= 20:

        score += 15

    elif active_hotspots >= 10:

        score += 10

    elif active_hotspots >= 5:

        score += 5

    # =====================================
    # FINAL CAP
    # =====================================

    return min(score, 100)

# =====================================
# RISK CLASSIFICATION
# =====================================

def classify_risk_level(

    threat_score
):

    if threat_score >= 85:

        return "CRITICAL"

    elif threat_score >= 65:

        return "HIGH"

    elif threat_score >= 40:

        return "MODERATE"

    else:

        return "LOW"

# =====================================
# HOTSPOT PRIORITY ENGINE
# =====================================

def build_hotspot_priority_table(

    cluster_df
):

    # =====================================
    # EMPTY SAFETY
    # =====================================

    if (

        cluster_df.empty
        or
        'Cluster' not in cluster_df.columns

    ):

        return pd.DataFrame()

    # =====================================
    # CLUSTER COUNTS
    # =====================================

    hotspot_table = (

        cluster_df
        .groupby('Cluster')
        .size()
        .reset_index(name='Crime_Count')
        .sort_values(
            'Crime_Count',
            ascending=False
        )
    )

    # =====================================
    # PRIORITY LEVELS
    # =====================================

    hotspot_table['Priority_Level'] = (

        hotspot_table['Crime_Count']
        .apply(

            lambda x:

            'CRITICAL'

            if x >= 500

            else (

                'HIGH'

                if x >= 250

                else (

                    'MODERATE'

                    if x >= 100

                    else 'LOW'
                )
            )
        )
    )

    # =====================================
    # RENAME
    # =====================================

    hotspot_table.rename(

        columns={

            'Cluster': 'Hotspot_Zone'
        },

        inplace=True
    )

    return hotspot_table

# =====================================
# CRIME VOLATILITY ENGINE
# =====================================

def calculate_crime_volatility(

    forecast_df
):

    # =====================================
    # EMPTY SAFETY
    # =====================================

    if (

        forecast_df.empty
        or
        'Predicted_Crime_Count'
        not in forecast_df.columns

    ):

        return {

            "volatility_score": 0,

            "volatility_level": "STABLE"
        }

    # =====================================
    # STANDARD DEVIATION
    # =====================================

    volatility_score = round(

        forecast_df[
            'Predicted_Crime_Count'
        ].std(),

        2
    )

    # =====================================
    # CLASSIFICATION
    # =====================================

    if volatility_score >= 100:

        volatility_level = "EXTREME"

    elif volatility_score >= 50:

        volatility_level = "HIGH"

    elif volatility_score >= 20:

        volatility_level = "MODERATE"

    else:

        volatility_level = "STABLE"

    return {

        "volatility_score": volatility_score,

        "volatility_level": volatility_level
    }

# =====================================
# EXECUTIVE INTELLIGENCE ENGINE
# =====================================

def generate_executive_summary(

    threat_level,
    threat_score,
    volatility_level,
    anomaly_count,
    active_hotspots
):

    summary = []

    # =====================================
    # THREAT SUMMARY
    # =====================================

    summary.append(

        f"Current national intelligence threat level is {threat_level} with operational score of {threat_score}/100."
    )

    # =====================================
    # VOLATILITY
    # =====================================

    summary.append(

        f"Crime volatility assessment currently classified as {volatility_level}."
    )

    # =====================================
    # ANOMALIES
    # =====================================

    summary.append(

        f"AI systems identified {anomaly_count} active anomaly events requiring operational review."
    )

    # =====================================
    # HOTSPOTS
    # =====================================

    summary.append(

        f"{active_hotspots} active hotspot zones currently under geographic surveillance."
    )

    # =====================================
    # FINAL RECOMMENDATION
    # =====================================

    if threat_level in ['CRITICAL', 'HIGH']:

        summary.append(

            "Immediate tactical deployment and predictive intervention recommended."
        )

    else:

        summary.append(

            "Current intelligence posture remains under controlled monitoring."
        )

    return summary