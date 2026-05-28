import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/final_cleaned_crime_data.csv")

# Monthly aggregation
monthly_crime = df.groupby(['YEAR', 'MONTH']).size().reset_index(name='Crime_Count')

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

monthly_crime['Prev_Month_Crime'] = (
    monthly_crime['Crime_Count']
    .shift(1)
)

monthly_crime['Rolling_Avg_3'] = (
    monthly_crime['Crime_Count']
    .shift(1)
    .rolling(window=3)
    .mean()
)

monthly_crime['Crime_Change'] = (
    monthly_crime['Crime_Count']
    .diff()
    .shift(1)
)

monthly_crime = monthly_crime.dropna()

# -----------------------------
# FEATURES & TARGET
# -----------------------------

X = monthly_crime[
    [
        'YEAR',
        'MONTH',
        'Prev_Month_Crime',
        'Rolling_Avg_3',
        'Crime_Change'
    ]
]

y = monthly_crime['Crime_Count']

# -----------------------------
# TRAIN MODEL
# -----------------------------

model = LinearRegression()

model.fit(X, y)

# -----------------------------
# FUTURE FORECASTING
# -----------------------------

# Get latest known values
last_row = monthly_crime.iloc[-1]

prev_crime = last_row['Crime_Count']
rolling_avg = last_row['Rolling_Avg_3']
crime_change = last_row['Crime_Change']

# Create future months
future_data = []

future_year = 2012
future_months = range(1, 13)

for month in future_months:

    future_features = {
        'YEAR': future_year,
        'MONTH': month,
        'Prev_Month_Crime': prev_crime,
        'Rolling_Avg_3': rolling_avg,
        'Crime_Change': crime_change
    }

    # Predict future crime
    prediction = model.predict(pd.DataFrame([future_features]))[0]

    # Save result
    future_data.append({
        'YEAR': future_year,
        'MONTH': month,
        'Predicted_Crime_Count': round(prediction)
    })

    # Update rolling values for next prediction
    crime_change = prediction - prev_crime
    prev_crime = prediction
    rolling_avg = (
        rolling_avg + prediction
    ) / 2

# -----------------------------
# CREATE FORECAST DATAFRAME
# -----------------------------

forecast_df = pd.DataFrame(future_data)

print("\nFuture Crime Forecasts:")
print(forecast_df)

# Save predictions
forecast_df.to_csv(
    "ml/outputs/future_crime_predictions.csv",
    index=False
)

# -----------------------------
# VISUALIZATION
# -----------------------------

plt.figure(figsize=(12,6))

# Historical data
plt.plot(
    monthly_crime['Crime_Count'].values,
    label='Historical Crime'
)

# Future predictions
future_x = range(
    len(monthly_crime),
    len(monthly_crime) + len(forecast_df)
)

plt.plot(
    future_x,
    forecast_df['Predicted_Crime_Count'],
    label='Forecasted Crime',
    linestyle='dashed'
)

plt.title("Future Crime Forecasting")
plt.xlabel("Time")
plt.ylabel("Crime Count")

plt.legend()

# Save chart
plt.savefig(
    "ml/outputs/future_crime_forecast.png"
)

plt.show()

print("\nFuture forecasting completed successfully!")