import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/final_cleaned_crime_data.csv")

# -----------------------------
# SELECT COORDINATES
# -----------------------------
coordinates = df[['Latitude', 'Longitude']]

# Remove missing values
coordinates = coordinates.dropna()

# Remove invalid coordinates
coordinates = coordinates[
    (coordinates['Latitude'] >= 49.0) &
    (coordinates['Latitude'] <= 49.35) &
    (coordinates['Longitude'] >= -123.3) &
    (coordinates['Longitude'] <= -122.9)
]

# -----------------------------
# K-MEANS CLUSTERING
# -----------------------------

# Number of clusters
k = 5

kmeans = KMeans(
    n_clusters=k,
    random_state=42
)

# Train clustering model
coordinates['Cluster'] = kmeans.fit_predict(coordinates)

# -----------------------------
# VISUALIZATION
# -----------------------------

plt.figure(figsize=(12,8))

scatter = plt.scatter(
    coordinates['Longitude'],
    coordinates['Latitude'],
    c=coordinates['Cluster'],
    cmap='viridis',
    s=10
)

plt.title("Crime Hotspot Clusters")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.colorbar(scatter, label='Cluster')

# Save figure
plt.savefig(
    "ml/outputs/crime_hotspot_clusters.png"
)

plt.show()

# -----------------------------
# SAVE CLUSTER DATA
# -----------------------------

coordinates.to_csv(
    "ml/outputs/crime_hotspot_clusters.csv",
    index=False
)

print("\nHotspot clustering completed successfully!")