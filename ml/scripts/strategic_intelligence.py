import pandas as pd

# =====================================
# LOAD DATA
# =====================================

forecast_df = pd.read_csv(
    r"D:\FBI_Crime_Project\ml\outputs\future_crime_predictions.csv"
)

risk_df = pd.read_csv(
    r"D:\FBI_Crime_Project\ml\outputs\hotspot_risk_scores.csv"
)

anomaly_df = pd.read_csv(
    r"D:\FBI_Crime_Project\ml\outputs\crime_anomalies.csv"
)

# =====================================
# FORECAST ANALYSIS
# =====================================

first_forecast = forecast_df.iloc[0][
    'Predicted_Crime_Count'
]

last_forecast = forecast_df.iloc[-1][
    'Predicted_Crime_Count'
]

if last_forecast < first_forecast:

    forecast_message = (
        "Crime activity is forecasted "
        "to decline through 2012."
    )

else:

    forecast_message = (
        "Crime activity is forecasted "
        "to increase through 2012."
    )

# =====================================
# HOTSPOT ANALYSIS
# =====================================

top_risk = risk_df.iloc[0]

hotspot_message = (
    f"{top_risk['Cluster_Name']} "
    f"remains the highest-risk "
    f"crime zone."
)

# =====================================
# ANOMALY ANALYSIS
# =====================================

anomalies = anomaly_df[
    anomaly_df['Anomaly_Label'] == 'Anomaly'
]

anomaly_message = (
    f"Sentinel AI detected "
    f"{len(anomalies)} abnormal "
    f"crime periods."
)

# =====================================
# EARLIEST THREAT
# =====================================

first_alert = anomalies.iloc[0]

threat_message = (
    f"Threat concentration peaked "
    f"during {int(first_alert['YEAR'])}-"
    f"{int(first_alert['MONTH'])}."
)

# =====================================
# BUILD REPORT
# =====================================

report = f"""
AI STRATEGIC INTELLIGENCE REPORT

• {forecast_message}

• {hotspot_message}

• {anomaly_message}

• {threat_message}
"""

# =====================================
# SAVE REPORT
# =====================================

with open(
    r"D:\FBI_Crime_Project\ml\outputs\strategic_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

# =====================================
# DISPLAY REPORT
# =====================================

print(report)

print(
    "\nStrategic intelligence report generated successfully!"
)