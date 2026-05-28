import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# LOAD CLUSTER DATA
# -----------------------------

df = pd.read_csv(
    "ml/outputs/crime_hotspot_clusters.csv"
)

# -----------------------------
# COUNT CRIMES PER CLUSTER
# -----------------------------

cluster_counts = (
    df['Cluster']
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    'Cluster',
    'Crime_Count'
]

# -----------------------------
# SORT BY DANGER
# -----------------------------

cluster_counts = cluster_counts.sort_values(
    by='Crime_Count',
    ascending=False
)

# -----------------------------
# ASSIGN RISK LEVELS
# -----------------------------

risk_labels = []

for count in cluster_counts['Crime_Count']:

    if count > 100000:
        risk_labels.append("Extreme")

    elif count > 80000:
        risk_labels.append("High")

    elif count > 50000:
        risk_labels.append("Medium")

    else:
        risk_labels.append("Low")

cluster_counts['Risk_Level'] = risk_labels

# -----------------------------
# AI CLUSTER NAMES
# -----------------------------

cluster_names = {
    0: "Downtown High Risk Zone",
    1: "East Crime Corridor",
    2: "Extreme Hotspot Zone",
    3: "Commercial Theft Sector",
    4: "Residential Risk Area"
}

cluster_counts['Cluster_Name'] = (
    cluster_counts['Cluster']
    .map(cluster_names)
)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\nCluster Risk Intelligence:\n")
print(cluster_counts)

# -----------------------------
# SAVE RESULTS
# -----------------------------

cluster_counts.to_csv(
    "ml/outputs/hotspot_risk_scores.csv",
    index=False
)

# -----------------------------
# VISUALIZATION
# -----------------------------

plt.figure(figsize=(12,7))

bars = plt.bar(
    cluster_counts['Cluster_Name'],
    cluster_counts['Crime_Count'],
    color='crimson'
)

plt.title("AI Crime Hotspot Risk Scores")

plt.xlabel("Cluster Intelligence Zone")
plt.ylabel("Crime Count")

plt.xticks(rotation=15)

# -----------------------------
# LABELS ON BARS
# -----------------------------

for bar, label in zip(
    bars,
    cluster_counts['Risk_Level']
):

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        label,
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# -----------------------------
# SAVE FIGURE
# -----------------------------

plt.savefig(
    "ml/outputs/hotspot_risk_scores.png"
)

plt.show()

print("\nRisk scoring completed successfully!")