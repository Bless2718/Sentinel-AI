from flask import Blueprint, render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from website.utils.dataset_profiler import (
    profile_dataset
)

from website.utils.data_loader import (
    build_analytics_data,
    PLOT_LAYOUT,
    AXIS_STYLE,
    LEGEND_STYLE
)

# =====================================
# CREATE BLUEPRINT
# =====================================

time_bp = Blueprint(
    "time_intelligence",
    __name__
)

# =====================================
# CHART CONFIG
# =====================================

CHART_CONFIG = dict(
    displayModeBar=False,
    responsive=True
)


def empty_temporal_fig(
    title="Temporal Intelligence",
    message="No temporal intelligence available",
    height=500
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
        height=height,
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    return fig


# =====================================
# ROUTE
# =====================================

@time_bp.route("/time-intelligence")
@login_required
def time_intelligence():

    # =====================================
    # BUILD DYNAMIC ANALYTICS DATA
    # =====================================

    data = build_analytics_data()

    master_df = data['master_df']

    forecast_df = data['forecast_df']

    anomaly_df = data['anomaly_df']

    cluster_df = data['cluster_df']

    risk_df = data['risk_df']

    # =====================================
    # LOCAL DATA COPIES
    # =====================================

    local_master_df = master_df.copy()

    local_forecast_df = forecast_df.copy()

    local_anomaly_df = anomaly_df.copy()

    # =====================================
    # DATASET PROFILE
    # =====================================

    profile = profile_dataset(
        local_master_df
    )

    # =====================================
    # SAFE TIME DATA VALIDATION
    # =====================================

    time_data_available = (
        not local_master_df.empty
        and
        'YEAR' in local_master_df.columns
    )

    month_data_available = (
        not local_master_df.empty
        and
        'MONTH' in local_master_df.columns
    )

    date_data_available = (
        not local_master_df.empty
        and
        'DATE' in local_master_df.columns
    )

    if time_data_available:

        local_master_df['YEAR'] = pd.to_numeric(
            local_master_df['YEAR'],
            errors='coerce'
        )

        time_data_available = (
            not local_master_df['YEAR']
            .dropna()
            .empty
        )

    if month_data_available:

        local_master_df['MONTH'] = pd.to_numeric(
            local_master_df['MONTH'],
            errors='coerce'
        )

        month_data_available = (
            not local_master_df['MONTH']
            .dropna()
            .empty
        )

    if date_data_available:

        local_master_df['DATE'] = pd.to_datetime(
            local_master_df['DATE'],
            errors='coerce'
        )

        date_data_available = (
            not local_master_df['DATE']
            .dropna()
            .empty
        )

    # =====================================
    # KPI VALUES
    # =====================================

    # =====================================
    # PEAK HOUR
    # =====================================

    if (

        'HOUR' in local_master_df.columns

        and

        not local_master_df['HOUR'].dropna().empty
    ):

        hourly_crime = (

            local_master_df['HOUR']
            .value_counts()
        )

        if not hourly_crime.empty:

            peak_hour = hourly_crime.idxmax()

        else:

            peak_hour = "No Data"

    else:

        peak_hour = "No Data"

    if month_data_available:

        monthly_counts = (

            local_master_df['MONTH']
            .dropna()
            .value_counts()
        )

        if not monthly_counts.empty:

            peak_month = int(
                monthly_counts.idxmax()
            )

        else:

            peak_month = "N/A"

    else:

        peak_month = "N/A"

    # =====================================
    # PEAK YEAR
    # =====================================

    if time_data_available:

        yearly_counts = (

            local_master_df['YEAR']
            .dropna()
            .value_counts()
        )

        if not yearly_counts.empty:

            peak_year = int(
                yearly_counts.idxmax()
            )

        else:

            peak_year = "N/A"

    else:

        peak_year = "N/A"

    # =====================================
    # FORECAST DIRECTION
    # =====================================

    forecast_data_available = (
        not local_forecast_df.empty
        and
        'Date' in local_forecast_df.columns
        and
        'Predicted_Crime_Count' in local_forecast_df.columns
    )

    if (

        forecast_data_available

        and

        not local_forecast_df.empty
    ):

        local_forecast_df['Date'] = pd.to_datetime(

            local_forecast_df['Date'],

            errors='coerce'
        )

        local_forecast_df = local_forecast_df.dropna(

            subset=['Predicted_Crime_Count']
        )

        forecast_data_available = (
            not local_forecast_df.empty
        )

        if len(local_forecast_df) > 1:

            latest_forecast = local_forecast_df[
                'Predicted_Crime_Count'
            ].iloc[-1]

            earliest_forecast = local_forecast_df[
                'Predicted_Crime_Count'
            ].iloc[0]

            if latest_forecast > earliest_forecast:

                forecast_direction = "Increasing"

            elif latest_forecast < earliest_forecast:

                forecast_direction = "Declining"

            else:

                forecast_direction = "Stable"

        else:

            forecast_direction = "Insufficient Data"

    else:

        forecast_direction = "N/A"

    # =====================================
    # THREAT PERIODS
    # =====================================

    anomaly_data_available = (
        not local_anomaly_df.empty
        and
        'Date' in local_anomaly_df.columns
        and
        'Crime_Count' in local_anomaly_df.columns
        and
        'Anomaly_Label' in local_anomaly_df.columns
    )

    if anomaly_data_available:

        local_anomaly_df['Date'] = pd.to_datetime(
            local_anomaly_df['Date'],
            errors='coerce'
        )

        local_anomaly_df = local_anomaly_df.dropna(
            subset=['Date', 'Crime_Count']
        )

        if local_anomaly_df['Anomaly_Label'].dtype != 'object':

            local_anomaly_df['Anomaly_Label'] = local_anomaly_df[
                'Anomaly_Label'
            ].astype(str)

        anomaly_data_available = (
            not local_anomaly_df.empty
        )

        if anomaly_data_available:

            threat_periods = len(
                local_anomaly_df[
                    local_anomaly_df['Anomaly_Label']
                    .str.contains("1|Anomaly", case=False, na=False)
                ]
            )

        else:

            threat_periods = 0

    else:

        threat_periods = 0

    # =====================================
    # YEARLY TREND
    # =====================================

    if time_data_available:

        yearly_trend = (
            local_master_df
            .dropna(
                subset=['YEAR']
            )
            .groupby('YEAR')
            .size()
            .reset_index(name='Crime_Count')
        )

        if yearly_trend.empty:

            yearly_fig = empty_temporal_fig(
                title='Yearly Crime Intelligence',
                height=600
            )

        else:

            yearly_fig = px.line(
                yearly_trend,
                x='YEAR',
                y='Crime_Count',
                markers=True
            )

            yearly_fig.update_traces(
                line=dict(
                    width=4,
                    color='#8b5cf6'
                ),
                marker=dict(
                    size=8
                )
            )

            yearly_fig.update_layout(
                title='Yearly Crime Intelligence',
                height=600,
                hovermode='x unified',
                xaxis_title='Year',
                yaxis_title='Crime Volume',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

    else:

        yearly_fig = empty_temporal_fig(
            title='Yearly Crime Intelligence',
            height=600
        )

    yearly_graph = yearly_fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config=CHART_CONFIG
    )

    # =====================================
    # MONTHLY TREND
    # =====================================

    if month_data_available:

        monthly_trend = (
            local_master_df
            .dropna(
                subset=['MONTH']
            )
            .groupby('MONTH')
            .size()
            .reset_index(name='Crime_Count')
        )

        if monthly_trend.empty:

            monthly_fig = empty_temporal_fig(
                title='Monthly Crime Distribution'
            )

        else:

            monthly_fig = px.bar(
                monthly_trend,
                x='MONTH',
                y='Crime_Count',
                color='Crime_Count',
                text_auto=True
            )

            monthly_fig.update_layout(
                title='Monthly Crime Distribution',
                height=500,
                xaxis_title='Month',
                yaxis_title='Crime Volume',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                coloraxis_showscale=False,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

    else:

        monthly_fig = empty_temporal_fig(
            title='Monthly Crime Distribution'
        )

    monthly_graph = monthly_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # FORECAST CHART
    # =====================================

    if forecast_data_available:

        forecast_fig = px.line(
            local_forecast_df,
            x='Date',
            y='Predicted_Crime_Count',
            markers=True
        )

        forecast_fig.update_traces(
            line=dict(
                width=4,
                color='#22c55e'
            ),
            marker=dict(
                size=7
            )
        )

        forecast_fig.update_layout(
            title='AI Forecast Timeline',
            height=600,
            hovermode='x unified',
            xaxis_title='Forecast Timeline',
            yaxis_title='Predicted Crime Count',
            xaxis=AXIS_STYLE,
            yaxis=AXIS_STYLE,
            legend=LEGEND_STYLE,
            **PLOT_LAYOUT
        )

    else:

        forecast_fig = empty_temporal_fig(
            title='AI Forecast Timeline',
            message='No forecast intelligence available',
            height=600
        )

    forecast_graph = forecast_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # ANOMALY DETECTION
    # =====================================

    if anomaly_data_available:

        if local_anomaly_df.empty:

            anomaly_fig = empty_temporal_fig(
                title='Temporal Threat Detection',
                message='No anomaly intelligence available',
                height=600
            )

        else:

            anomaly_fig = px.scatter(
                local_anomaly_df,
                x='Date',
                y='Crime_Count',
                color='Anomaly_Label'
            )

            anomaly_fig.update_traces(
                marker=dict(
                    size=10
                )
            )

            anomaly_fig.update_layout(
                title='Temporal Threat Detection',
                height=600,
                hovermode='x unified',
                xaxis_title='Timeline',
                yaxis_title='Crime Activity',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

    else:

        anomaly_fig = empty_temporal_fig(
            title='Temporal Threat Detection',
            message='No anomaly intelligence available',
            height=600
        )

    anomaly_graph = anomaly_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # QUARTERLY INTELLIGENCE
    # =====================================

    if (

        date_data_available

        and

        'DATE' in local_master_df.columns

        and

        not local_master_df['DATE'].dropna().empty
    ):

        quarterly_trend = (
            local_master_df
            .dropna(
                subset=['DATE']
            )
            .groupby(
                pd.Grouper(
                    key='DATE',
                    freq='QE'
                )
            )
            .size()
            .reset_index(name='Crime_Count')
        )

        if quarterly_trend.empty:

            quarterly_fig = empty_temporal_fig(
                title='Quarterly Crime Intelligence'
            )

        else:

            quarterly_fig = px.area(
                quarterly_trend,
                x='DATE',
                y='Crime_Count'
            )

            quarterly_fig.update_traces(
                line=dict(
                    color='#06b6d4',
                    width=3
                )
            )

            quarterly_fig.update_layout(
                title='Quarterly Crime Intelligence',
                height=500,
                hovermode='x unified',
                xaxis_title='Quarter',
                yaxis_title='Crime Volume',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

    else:

        quarterly_fig = empty_temporal_fig(
            title='Quarterly Crime Intelligence'
        )

    quarterly_graph = quarterly_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # RENDER TEMPLATE
    # =====================================

    return render_template(
        "pages/time_intelligence.html",
        peak_year=peak_year,
        profile=profile,
        peak_hour=peak_hour,
        peak_month=peak_month,
        forecast_direction=forecast_direction,
        threat_periods=threat_periods,
        yearly_graph=yearly_graph,
        monthly_graph=monthly_graph,
        forecast_graph=forecast_graph,
        anomaly_graph=anomaly_graph,
        quarterly_graph=quarterly_graph
    )