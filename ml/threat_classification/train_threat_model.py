import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (

    classification_report,
    confusion_matrix,
    accuracy_score
)

from xgboost import XGBClassifier

import joblib

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(

    "D:/FBI_Crime_Project/ml/outputs/"
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
# TARGET
# =========================================

y = df['THREAT_LEVEL']

# =========================================
# LABEL ENCODING
# =========================================

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

# =========================================
# TRAIN TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y_encoded,

    test_size=0.2,

    random_state=42,

    stratify=y_encoded
)

# =========================================
# XGBOOST MODEL
# =========================================

print("TRAINING THREAT CLASSIFIER...\n")

model = XGBClassifier(

    n_estimators=300,

    max_depth=6,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    objective='multi:softmax',

    num_class=3,

    random_state=42
)

# =========================================
# TRAIN
# =========================================

model.fit(

    X_train,
    y_train
)

print("MODEL TRAINING COMPLETE\n")

# =========================================
# PREDICTIONS
# =========================================

predictions = model.predict(X_test)

# =========================================
# EVALUATION
# =========================================

accuracy = accuracy_score(

    y_test,
    predictions
)

print(f"ACCURACY: {accuracy:.4f}\n")

print("CLASSIFICATION REPORT:\n")

print(

    classification_report(
        y_test,
        predictions
    )
)

print("CONFUSION MATRIX:\n")

print(

    confusion_matrix(
        y_test,
        predictions
    )
)

# =========================================
# SAVE MODEL
# =========================================

model_path = (

    "D:/FBI_Crime_Project/ml/models/"
    "threat_classifier.pkl"
)

encoder_path = (

    "D:/FBI_Crime_Project/ml/models/"
    "threat_label_encoder.pkl"
)

joblib.dump(

    model,
    model_path
)

joblib.dump(

    encoder,
    encoder_path
)

print("\nMODEL SAVED:\n")

print(model_path)

print("\nENCODER SAVED:\n")

print(encoder_path)