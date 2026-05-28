import pandas as pd

from prophet import Prophet

# =====================================
# GENERATE PROPHET FORECAST
# =====================================

def generate_prophet_forecast(df):

    # =====================================
    # EMPTY SAFETY
    # =====================================

    if df.empty:

        return pd.DataFrame()

    if 'DATE' not in df.columns:

        return pd.DataFrame()

    # =====================================
    # COPY DATA
    # =====================================

    local_df = df.copy()

    # =====================================
    # CLEAN DATES
    # =====================================

    local_df['DATE'] = pd.to_datetime(

        local_df['DATE'],

        errors='coerce'
    )

    local_df.dropna(

        subset=['DATE'],

        inplace=True
    )

    # =====================================
    # DAILY CRIME COUNTS
    # =====================================

    trend_df = (

        local_df
        .groupby('DATE')
        .size()
        .reset_index(name='y')
    )

    # =====================================
    # PROPHET FORMAT
    # =====================================

    trend_df.rename(

        columns={
            'DATE': 'ds'
        },

        inplace=True
    )

    # =====================================
    # TRAIN MODEL
    # =====================================

    model = Prophet(

        daily_seasonality=True,

        weekly_seasonality=True,

        yearly_seasonality=True
    )

    model.fit(

        trend_df
    )

    # =====================================
    # FUTURE DATES
    # =====================================

    future = model.make_future_dataframe(

        periods=30
    )

    # =====================================
    # PREDICT
    # =====================================

    forecast = model.predict(

        future
    )

    # =====================================
    # FINAL OUTPUT
    # =====================================

    forecast_df = forecast[[

        'ds',
        'yhat',
        'yhat_lower',
        'yhat_upper'
    ]].copy()

    forecast_df.rename(

        columns={

            'ds': 'Date',

            'yhat': 'Predicted_Crime_Count',

            'yhat_lower': 'Lower_Bound',

            'yhat_upper': 'Upper_Bound'
        },

        inplace=True
    )

    return forecast_df