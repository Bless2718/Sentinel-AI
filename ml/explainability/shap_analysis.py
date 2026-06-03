import pandas as pd

import joblib

import shap

import matplotlib.pyplot as plt

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(

    "(__file__).resolve().parents[2]/ml/outputs/"
    "threat_classification_dataset.csv"
)

print("\nTHREAT DATASET LOADED\n")

# =========================================
# FEATURES
# =========================================

features = [

    'CRIME_COUNT',
    'ROLLING_MEAN_3',
    'ROLLING_STD_3',
    'LAG_1',
    'LAG_2',
    'LAG_3',
    'VOLATILITY',
    'ANOMALY',
    'ANOMALY_SCORE'
]

X = df[features]

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load(

    "(__file__).resolve().parents[2]/ml/models/"
    "threat_classifier.pkl"
)

print("THREAT MODEL LOADED\n")

# =========================================
# SHAP EXPLAINER
# =========================================

print("GENERATING SHAP EXPLANATIONS...\n")

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

# =========================================
# SUMMARY PLOT
# =========================================

plt.figure(figsize=(12, 8))

shap.summary_plot(

    shap_values,
    X,

    show=False
)

# =========================================
# SAVE PLOT
# =========================================

output_path = (

    "(__file__).resolve().parents[2]/ml/outputs/"
    "shap_summary.png"
)

plt.savefig(

    output_path,

    bbox_inches='tight',

    dpi=300
)

print("SHAP SUMMARY SAVED:\n")

print(output_path)

# =========================================
# BAR IMPORTANCE PLOT
# =========================================

plt.figure(figsize=(12, 8))

shap.summary_plot(

    shap_values,
    X,

    plot_type="bar",

    show=False
)

bar_output = (

    "(__file__).resolve().parents[2]/ml/outputs/"
    "shap_feature_importance.png"
)

plt.savefig(

    bar_output,

    bbox_inches='tight',

    dpi=300
)

print("\nFEATURE IMPORTANCE SAVED:\n")

print(bar_output)

print("\nEXPLAINABLE AI ANALYSIS COMPLETE")