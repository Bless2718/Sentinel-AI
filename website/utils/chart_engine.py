import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from utils.data_loader import (
    COLORS,
    PLOT_LAYOUT,
    AXIS_STYLE,
    LEGEND_STYLE,
    MAPBOX_STYLE,
    safe_sample
)

# =====================================
# CHART CONFIG
# =====================================

CHART_CONFIG = dict(

    displayModeBar=False,

    responsive=True
)

# =====================================
# SAFE DATAFRAME SANITIZER
# =====================================

def sanitize_dataframe(

    df,

    required_columns=None,

    numeric_columns=None,

    datetime_columns=None
):

    if df is None or df.empty:

        return pd.DataFrame()

    local_df = df.copy()

    # =====================================
    # REQUIRED COLUMNS
    # =====================================

    if required_columns:

        for column in required_columns:

            if column not in local_df.columns:

                return pd.DataFrame()

    # =====================================
    # NUMERIC SANITATION
    # =====================================

    if numeric_columns:

        for column in numeric_columns:

            if column in local_df.columns:

                local_df[column] = pd.to_numeric(

                    local_df[column],

                    errors='coerce'
                )

    # =====================================
    # DATETIME SANITATION
    # =====================================

    if datetime_columns:

        for column in datetime_columns:

            if column in local_df.columns:

                local_df[column] = pd.to_datetime(

                    local_df[column],

                    errors='coerce'
                )

    # =====================================
    # DROP INVALIDS
    # =====================================

    local_df = local_df.replace(

        [np.inf, -np.inf],

        np.nan
    )

    local_df = local_df.dropna(how='all')

    return local_df

# =====================================
# EMPTY CHART
# =====================================

def empty_chart(

    title,
    message="No data available"
):

    fig = go.Figure()

    fig.add_annotation(

        text=message,

        x=0.5,
        y=0.5,

        showarrow=False,

        font=dict(
            size=20,
            color="white"
        ),

        xref="paper",
        yref="paper"
    )

    fig.update_layout(

        title=title,

        height=500,

        **PLOT_LAYOUT
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config=CHART_CONFIG
    )

# =====================================
# EMPTY HTML BLOCK
# =====================================

def empty_html_block(

    message="No intelligence available"
):

    return f"""

    <div class="empty-state">

        {message}

    </div>

    """

# =====================================
# SAFE SORT
# =====================================

def safe_sort(

    df,

    column,

    ascending=False
):

    if (
        df.empty
        or
        column not in df.columns
    ):

        return pd.DataFrame()

    return df.sort_values(

        by=column,

        ascending=ascending
    )

# =====================================
# YEARLY TREND CHART
# =====================================

def build_yearly_trend_chart(

    filtered_df
):

    filtered_df = sanitize_dataframe(

        filtered_df,

        required_columns=['YEAR']
    )

    if filtered_df.empty:

        return empty_chart(

            "Crime Trend Intelligence"
        )

    yearly_trend = (

        filtered_df
        .groupby('YEAR')
        .size()
        .reset_index(name='Crime_Count')
    )

    if yearly_trend.empty:

        return empty_chart(

            "Crime Trend Intelligence"
        )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=yearly_trend['YEAR'],

            y=yearly_trend['Crime_Count'],

            mode='lines+markers',

            line=dict(
                color='#8b5cf6',
                width=4
            ),

            marker=dict(
                size=8
            ),

            fill='tozeroy',

            fillcolor='rgba(139,92,246,0.12)',

            name='Crime Activity'
        )
    )

    fig.update_layout(

        title='Crime Trend Intelligence',

        height=500,

        hovermode='x unified',

        xaxis_title='Year',

        yaxis_title='Crime Count',

        xaxis=AXIS_STYLE,

        yaxis=AXIS_STYLE,

        legend=LEGEND_STYLE,

        **PLOT_LAYOUT
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config=CHART_CONFIG
    )

# =====================================
# FORECAST CHART
# =====================================

def build_forecast_chart(

    forecast_df
):

    forecast_df = sanitize_dataframe(

        forecast_df,

        required_columns=[
            'Date',
            'Predicted_Crime_Count'
        ],

        numeric_columns=[
            'Predicted_Crime_Count',
            'Upper_Bound',
            'Lower_Bound'
        ],

        datetime_columns=[
            'Date'
        ]
    )

    if forecast_df.empty:

        return empty_chart(

            "Forecast Intelligence"
        )

    fig = go.Figure()

    # =====================================
    # CONFIDENCE BAND
    # =====================================

    if (

        'Upper_Bound'
        in forecast_df.columns

        and

        'Lower_Bound'
        in forecast_df.columns

        and

        not forecast_df[
            'Upper_Bound'
        ].dropna().empty

        and

        not forecast_df[
            'Lower_Bound'
        ].dropna().empty
    ):

        # =====================================
        # CONFIDENCE UPPER BOUND
        # =====================================

        fig.add_trace(

            go.Scatter(

                x=forecast_df['Date'],

                y=forecast_df['Upper_Bound'],

                line=dict(
                    width=0
                ),

                hoverinfo='skip',

                showlegend=False,

                mode='lines',

                name='Upper Bound'
            )
        )

        # =====================================
        # CONFIDENCE LOWER BOUND
        # =====================================

        fig.add_trace(

            go.Scatter(

                x=forecast_df['Date'],

                y=forecast_df['Lower_Bound'],

                fill='tonexty',

                fillcolor='rgba(139,92,246,0.18)',

                line=dict(
                    width=0
                ),

                hoverinfo='skip',

                showlegend=True,

                mode='lines',

                name='Forecast Confidence'
            )
        )

    # =====================================
    # MAIN FORECAST LINE
    # =====================================

    fig.add_trace(

        go.Scatter(

            x=forecast_df['Date'],

            y=forecast_df[
                'Predicted_Crime_Count'
            ],

            mode='lines+markers',

            line=dict(
                color='#8b5cf6',
                width=4
            ),

            marker=dict(
                size=7,
                color='#22c55e'
            ),

            name='AI Forecast'
        )
    )

    fig.update_layout(

        title='Forecast Intelligence',

        height=500,

        hovermode='x unified',

        xaxis_title='Timeline',

        yaxis_title='Predicted Crime Count',

        xaxis=AXIS_STYLE,

        yaxis=AXIS_STYLE,

        legend=LEGEND_STYLE,

        **PLOT_LAYOUT
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config=CHART_CONFIG
    )

# =====================================
# ANOMALY CHART
# =====================================

def build_anomaly_chart(

    anomaly_df
):

    anomaly_df = sanitize_dataframe(

        anomaly_df,

        required_columns=[
            'Date',
            'Crime_Count'
        ],

        numeric_columns=[
            'Crime_Count'
        ],

        datetime_columns=[
            'Date'
        ]
    )

    if anomaly_df.empty:

        return empty_chart(

            "Threat Detection Intelligence"
        )

    fig = px.scatter(

        anomaly_df,

        x='Date',

        y='Crime_Count',

        color=(

            'Anomaly_Label'

            if 'Anomaly_Label'
            in anomaly_df.columns

            else None
        )
    )

    fig.update_layout(

        title='Threat Detection Intelligence',

        height=500,

        hovermode='x unified',

        xaxis_title='Timeline',

        yaxis_title='Crime Activity',

        xaxis=AXIS_STYLE,

        yaxis=AXIS_STYLE,

        legend=LEGEND_STYLE,

        **PLOT_LAYOUT
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config=CHART_CONFIG
    )

# =====================================
# HOTSPOT MAP
# =====================================

def build_hotspot_map(

    cluster_df
):

    cluster_df = sanitize_dataframe(

        cluster_df,

        required_columns=[
            'Latitude',
            'Longitude'
        ],

        numeric_columns=[
            'Latitude',
            'Longitude'
        ]
    )

    if cluster_df.empty:

        return empty_chart(

            "Geographic Crime Intelligence"
        )

    cluster_df = cluster_df[

        (
            cluster_df['Latitude']
            .between(-90, 90)
        )

        &

        (
            cluster_df['Longitude']
            .between(-180, 180)
        )
    ]

    if cluster_df.empty:

        return empty_chart(

            "Geographic Crime Intelligence"
        )

    hotspot_sample = safe_sample(

        cluster_df,

        500
    )

    if hotspot_sample.empty:

        return empty_chart(

            "Geographic Crime Intelligence"
        )

    fig = px.scatter_map(

        hotspot_sample,

        lat='Latitude',

        lon='Longitude',

        color=(

            'Cluster'

            if 'Cluster'
            in hotspot_sample.columns

            else None
        ),

        zoom=9,

        height=600
    )

    fig.update_layout(

        title='Geographic Crime Intelligence',

        mapbox_style=MAPBOX_STYLE,

        legend=LEGEND_STYLE,

        **PLOT_LAYOUT
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config=CHART_CONFIG
    )