import pandas as pd

# -----------------------------
# LOAD FILES
# -----------------------------

model_results = pd.read_csv(
    "ml/outputs/model_comparison_results.csv"
)

risk_scores = pd.read_csv(
    "ml/outputs/hotspot_risk_scores.csv"
)

anomalies = pd.read_csv(
    "ml/outputs/crime_anomalies.csv"
)

forecast = pd.read_csv(
    "ml/outputs/future_crime_predictions.csv"
)

# -----------------------------
# MODEL INSIGHT
# -----------------------------

best_model = model_results.sort_values(
    by='R2',
    ascending=False
).iloc[0]

model_insight = (
    f"Best forecasting model: "
    f"{best_model['Model']} "
    f"with R2 Score of "
    f"{round(best_model['R2'], 3)}."
)

# -----------------------------
# HOTSPOT INSIGHT
# -----------------------------

highest_risk = risk_scores.iloc[0]

hotspot_insight = (
    f"Cluster {highest_risk['Cluster']} "
    f"is the most dangerous hotspot "
    f"with {highest_risk['Crime_Count']} crimes "
    f"and risk level "
    f"{highest_risk['Risk_Level']}."
)

# -----------------------------
# ANOMALY INSIGHT
# -----------------------------

anomaly_count = (
    anomalies['Anomaly_Label']
    .value_counts()
    .get('Anomaly', 0)
)

anomaly_insight = (
    f"The AI detected "
    f"{anomaly_count} abnormal crime periods "
    f"across the dataset."
)

# -----------------------------
# FORECAST INSIGHT
# -----------------------------

future_avg = (
    forecast['Predicted_Crime_Count']
    .mean()
)

forecast_insight = (
    f"Predicted future monthly crime average "
    f"is approximately "
    f"{round(future_avg)} crimes."
)

# -----------------------------
# COMBINE INSIGHTS
# -----------------------------

all_insights = [
    model_insight,
    hotspot_insight,
    anomaly_insight,
    forecast_insight
]

# -----------------------------
# DISPLAY INSIGHTS
# -----------------------------

print("\nAI GENERATED INSIGHTS:\n")

for insight in all_insights:
    print("-", insight)

# -----------------------------
# SAVE REPORT
# -----------------------------

with open(
    "ml/outputs/ai_generated_report.txt",
    "w"
) as file:

    file.write(
        "AI CRIME INTELLIGENCE REPORT\n\n"
    )

    for insight in all_insights:
        file.write(f"- {insight}\n")

print("\nAI insight report generated successfully!")