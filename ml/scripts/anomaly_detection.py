import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(
    "data/final_cleaned_crime_data.csv"
)

# -----------------------------
# MONTHLY CRIME COUNTS
# -----------------------------

monthly_crime = (
    df.groupby(['YEAR', 'MONTH'])
    .size()
    .reset_index(name='Crime_Count')
)

# -----------------------------
# CREATE FEATURES
# -----------------------------

X = monthly_crime[['Crime_Count']]

# -----------------------------
# TRAIN ISOLATION FOREST
# -----------------------------

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

monthly_crime['Anomaly'] = model.fit_predict(X)

# -----------------------------
# LABEL RESULTS
# -----------------------------

monthly_crime['Anomaly_Label'] = (
    monthly_crime['Anomaly']
    .map({
        1: 'Normal',
        -1: 'Anomaly'
    })
)

# -----------------------------
# SHOW ANOMALIES
# -----------------------------

anomalies = monthly_crime[
    monthly_crime['Anomaly_Label'] == 'Anomaly'
]

print("\nDetected Crime Anomalies:\n")
print(anomalies)

# -----------------------------
# SAVE RESULTS
# -----------------------------

monthly_crime.to_csv(
    "ml/outputs/crime_anomalies.csv",
    index=False
)

# -----------------------------
# VISUALIZATION
# -----------------------------

plt.figure(figsize=(12,6))

# Plot normal points
normal = monthly_crime[
    monthly_crime['Anomaly_Label'] == 'Normal'
]

plt.scatter(
    normal.index,
    normal['Crime_Count'],
    label='Normal'
)

# Plot anomalies
plt.scatter(
    anomalies.index,
    anomalies['Crime_Count'],
    color='red',
    label='Anomaly'
)

plt.title("Crime Anomaly Detection")
plt.xlabel("Time")
plt.ylabel("Crime Count")

plt.legend()

# Save figure
plt.savefig(
    "ml/outputs/crime_anomalies.png"
)

plt.show()

print("\nAnomaly detection completed successfully!")