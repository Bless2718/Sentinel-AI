import pandas as pd

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(

    "(__file__).resolve().parents[2]/ml/outputs/"
    "crime_anomalies_detected.csv"
)

print("\nANOMALY DATA LOADED\n")

# =========================================
# CREATE THREAT LABELS
# =========================================

high_threshold = (

    df['CRIME_COUNT']
    .quantile(0.90)
)

medium_threshold = (

    df['CRIME_COUNT']
    .quantile(0.70)
)

# =========================================
# LABEL FUNCTION
# =========================================

def classify_threat(row):

    crime_count = row['CRIME_COUNT']

    anomaly = row['ANOMALY']

    # HIGH THREAT
    if (
        crime_count >= high_threshold
        or anomaly == 1
    ):

        return "HIGH"

    # MEDIUM THREAT
    elif crime_count >= medium_threshold:

        return "MEDIUM"

    # LOW THREAT
    else:

        return "LOW"

# =========================================
# APPLY LABELS
# =========================================

df['THREAT_LEVEL'] = df.apply(

    classify_threat,

    axis=1
)

# =========================================
# RESULTS
# =========================================

print("THREAT LABEL DISTRIBUTION:\n")

print(

    df['THREAT_LEVEL']
    .value_counts()
)

# =========================================
# SAVE
# =========================================

output_path = (

    "(__file__).resolve().parents[2]/ml/outputs/"
    "threat_classification_dataset.csv"
)

df.to_csv(

    output_path,

    index=False
)

print("\nTHREAT DATASET SAVED:\n")

print(output_path)