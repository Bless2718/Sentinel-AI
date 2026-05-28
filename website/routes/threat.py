from flask import Blueprint, render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from website.utils.dataset_profiler import (
    profile_dataset
)

# =====================================
# IMPORT DATA
# =====================================

from website.utils.data_loader import (
    build_analytics_data,
    PLOT_LAYOUT,
    AXIS_STYLE,
    LEGEND_STYLE,
    MAPBOX_STYLE,
    TABLE_CLASSES,
    safe_sample
)

# =====================================
# CREATE BLUEPRINT
# =====================================

threat_bp = Blueprint(
    "threat",
    __name__
)

# =====================================
# CHART CONFIG
# =====================================

CHART_CONFIG = dict(
    displayModeBar=False,
    responsive=True
)


def empty_threat_fig(
    title="Threat Intelligence",
    message="No anomaly intelligence available",
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

@threat_bp.route("/threat-intelligence")
@login_required
def threat_intelligence():

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
    # DEBUG ANOMALY OUTPUT
    # =====================================

    print("\n========= ROUTE ANOMALY OUTPUT =========")
    print(anomaly_df.head())
    print(anomaly_df.columns)
    print(anomaly_df.empty)
    print("========================================\n")

    # =====================================
    # LOCAL DATA COPIES
    # =====================================

    local_anomaly_df = anomaly_df.copy()
    local_risk_df = risk_df.copy()
    local_cluster_df = cluster_df.copy()

    # =====================================
    # DATASET PROFILE
    # =====================================

    profile = profile_dataset(
        master_df
    )

    # =====================================
    # NORMALIZE RISK DATA
    # =====================================

    if (
        not local_risk_df.empty
        and
        'Crime_Count' in local_risk_df.columns
    ):

        local_risk_df['Crime_Count'] = pd.to_numeric(
            local_risk_df['Crime_Count'],
            errors='coerce'
        )

        local_risk_df = local_risk_df.dropna(
            subset=['Crime_Count']
        )

    if (
        not local_risk_df.empty
        and
        'Crime_Count' in local_risk_df.columns
        and
        'Risk_Score' not in local_risk_df.columns
    ):

        max_crime_count = local_risk_df['Crime_Count'].max()

        if max_crime_count and max_crime_count > 0:

            local_risk_df['Risk_Score'] = round(
                (
                    local_risk_df['Crime_Count']
                    /
                    max_crime_count
                ) * 100,
                2
            )

        else:

            local_risk_df['Risk_Score'] = 0

    if (
        not local_risk_df.empty
        and
        'Risk_Score' in local_risk_df.columns
    ):

        local_risk_df['Risk_Score'] = pd.to_numeric(
            local_risk_df['Risk_Score'],
            errors='coerce'
        ).fillna(0)

    if (
        not local_risk_df.empty
        and
        'Risk_Score' in local_risk_df.columns
        and
        'Risk_Level' not in local_risk_df.columns
    ):

        local_risk_df['Risk_Level'] = (
            local_risk_df['Risk_Score']
            .apply(
                lambda x:
                'HIGH'
                if x >= 75
                else 'MEDIUM'
                if x >= 40
                else 'LOW'
            )
        )

    # =====================================
    # SAFE ANOMALY VALIDATION
    # =====================================

    anomaly_data_available = (
        not local_anomaly_df.empty
        and
        'Anomaly_Label' in local_anomaly_df.columns
    )

    # =====================================
    # FALLBACK ANOMALY LABEL
    # =====================================

    if (
        not local_anomaly_df.empty
        and
        'Anomaly_Label' not in local_anomaly_df.columns
    ):

        if 'ANOMALY' in local_anomaly_df.columns:

            local_anomaly_df['Anomaly_Label'] = (
                local_anomaly_df['ANOMALY']
                .apply(
                    lambda x:
                    'Anomaly'
                    if x == -1
                    else 'Normal'
                )
            )

        else:

            local_anomaly_df['Anomaly_Label'] = 'Normal'

    anomaly_data_available = (
        not local_anomaly_df.empty
        and
        'Anomaly_Label' in local_anomaly_df.columns
    )

    if anomaly_data_available:

        local_anomaly_df['Anomaly_Label'] = (
            local_anomaly_df['Anomaly_Label']
            .astype(str)
            .str.strip()
        )

        local_anomaly_df = local_anomaly_df[
            local_anomaly_df['Anomaly_Label'] != ''
        ]

        anomaly_data_available = (
            not local_anomaly_df.empty
        )

    # =====================================
    # NORMALIZE DATE COLUMN
    # =====================================

    if (
        'DATE' not in local_anomaly_df.columns
        and
        'Date' in local_anomaly_df.columns
    ):

        local_anomaly_df['DATE'] = local_anomaly_df['Date']

    anomaly_chart_available = (
        anomaly_data_available
        and
        'DATE' in local_anomaly_df.columns
        and
        'Crime_Count' in local_anomaly_df.columns
    )

    if anomaly_chart_available:

        local_anomaly_df['DATE'] = pd.to_datetime(
            local_anomaly_df['DATE'],
            errors='coerce'
        )

        local_anomaly_df = local_anomaly_df.dropna(
            subset=['DATE']
        )

    if 'Crime_Count' in local_anomaly_df.columns:

        local_anomaly_df['Crime_Count'] = pd.to_numeric(
            local_anomaly_df['Crime_Count'],
            errors='coerce'
        )

        local_anomaly_df = local_anomaly_df.dropna(
            subset=[
                'Crime_Count'
            ]
        )

    anomaly_chart_available = (
        anomaly_data_available
        and
        not local_anomaly_df.empty
        and
        'DATE' in local_anomaly_df.columns
        and
        'Crime_Count' in local_anomaly_df.columns
    )

    anomaly_data = local_anomaly_df.copy()

    print(anomaly_data.head())
    print(anomaly_data.columns)
    print(anomaly_data.empty)

    # =====================================
    # CHART.JS ANOMALY PAYLOAD
    # =====================================

    if anomaly_chart_available:

        anomaly_chart_data = {
            "labels": anomaly_data['DATE']
                .dt.strftime('%Y-%m-%d')
                .tolist(),

            "datasets": [
                {
                    "label": "Crime Anomalies",
                    "data": anomaly_data['Crime_Count']
                        .tolist(),
                    "borderColor": "#a855f7",
                    "backgroundColor": "rgba(168,85,247,0.15)",
                    "fill": True,
                    "tension": 0.4,
                    "pointRadius": 0
                }
            ]
        }

    else:

        anomaly_chart_data = {
            "labels": [],
            "datasets": [
                {
                    "label": "Crime Anomalies",
                    "data": [],
                    "borderColor": "#a855f7",
                    "backgroundColor": "rgba(168,85,247,0.15)",
                    "fill": True,
                    "tension": 0.4,
                    "pointRadius": 0
                }
            ]
        }

    # =====================================
    # ALERT DATA
    # =====================================

    if anomaly_data_available:

        alert_df = anomaly_data[
            anomaly_data['Anomaly_Label']
            .str.contains("1|Anomaly", case=False, na=False)
        ]

        normal_df = anomaly_data[
            ~anomaly_data.index.isin(alert_df.index)
        ]

    else:

        alert_df = pd.DataFrame()
        normal_df = pd.DataFrame()

    # =====================================
    # THREAT SCORE
    # =====================================

    if (
        not alert_df.empty
        and
        'Crime_Count' in alert_df.columns
    ):

        average_threat_score = round(
            alert_df['Crime_Count'].mean(),
            2
        )

    else:

        average_threat_score = 0

    # =====================================
    # KPI VALUES
    # =====================================

    total_alerts = len(alert_df)
    active_anomalies = len(alert_df)

    if (
        not local_cluster_df.empty
        and
        'Cluster' in local_cluster_df.columns
    ):

        monitored_regions = local_cluster_df['Cluster'].nunique()

    else:

        monitored_regions = 0

    # =====================================
    # HIGHEST RISK ZONE
    # =====================================

    if (
        not local_risk_df.empty
        and
        'Crime_Count' in local_risk_df.columns
        and
        'Cluster_Name' in local_risk_df.columns
    ):

        sorted_risk_df = (
            local_risk_df
            .sort_values(
                by='Crime_Count',
                ascending=False
            )
        )

        if not sorted_risk_df.empty:

            highest_risk_zone = (
                sorted_risk_df.iloc[0]['Cluster_Name']
            )

        else:

            highest_risk_zone = "UNKNOWN"

    else:

        highest_risk_zone = "UNKNOWN"

    # =====================================
    # DYNAMIC THREAT LEVEL
    # =====================================

    if total_alerts > 25:

        threat_level = "CRITICAL"

    elif total_alerts > 15:

        threat_level = "HIGH"

    elif total_alerts > 5:

        threat_level = "MODERATE"

    else:

        threat_level = "LOW"

    # =====================================
    # THREAT DETECTION GRAPH
    # =====================================

    anomaly_graph = ""

    if not anomaly_data.empty:

        fig = px.line(

            anomaly_data,

            x='DATE',

            y='Crime_Count',

            color='Anomaly_Label',

            title='AI Threat Detection System',

            template='plotly_dark'
        )

        fig.update_layout(

            paper_bgcolor='#020617',

            plot_bgcolor='#020617',

            font=dict(color='white'),

            height=500
        )

        anomaly_graph = fig.to_html(

            full_html=False,

            include_plotlyjs='cdn'
        )

    # =====================================
    # RISK INTELLIGENCE GRAPH
    # =====================================

    risk_chart_available = (
        not local_risk_df.empty
        and
        'Cluster_Name' in local_risk_df.columns
        and
        'Crime_Count' in local_risk_df.columns
        and
        'Risk_Level' in local_risk_df.columns
    )

    if risk_chart_available:

        top_risks = (
            local_risk_df
            .sort_values(
                by='Crime_Count',
                ascending=False
            )
            .head(10)
        )

        risk_fig = px.bar(
            top_risks,
            x='Cluster_Name',
            y='Crime_Count',
            color='Risk_Level',
            text_auto=True
        )

        risk_fig.update_layout(
            title='Operational Risk Intelligence',
            height=600,
            xaxis_title='Operational Cluster',
            yaxis_title='Crime Activity',
            xaxis=AXIS_STYLE,
            yaxis=AXIS_STYLE,
            legend=LEGEND_STYLE,
            **PLOT_LAYOUT
        )

    else:

        risk_fig = empty_threat_fig(
            title='Operational Risk Intelligence',
            message='No risk intelligence available',
            height=600
        )

    risk_graph = risk_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # HEATMAP
    # =====================================

    heatmap_available = (
        not local_cluster_df.empty
        and
        'Latitude' in local_cluster_df.columns
        and
        'Longitude' in local_cluster_df.columns
    )

    if heatmap_available:

        local_cluster_df['Latitude'] = pd.to_numeric(
            local_cluster_df['Latitude'],
            errors='coerce'
        )

        local_cluster_df['Longitude'] = pd.to_numeric(
            local_cluster_df['Longitude'],
            errors='coerce'
        )

        local_cluster_df = local_cluster_df.dropna(
            subset=[
                'Latitude',
                'Longitude'
            ]
        )

        local_cluster_df = local_cluster_df[
            (
                local_cluster_df['Latitude']
                .between(-90, 90)
            )
            &
            (
                local_cluster_df['Longitude']
                .between(-180, 180)
            )
        ]

        heatmap_available = (
            not local_cluster_df.empty
        )

    if heatmap_available:

        hotspot_sample = safe_sample(
            local_cluster_df,
            8000
        )

        if hotspot_sample.empty:

            heatmap_available = False

    else:

        hotspot_sample = pd.DataFrame()

    if heatmap_available:

        heatmap_fig = px.density_map(
            hotspot_sample,
            lat='Latitude',
            lon='Longitude',
            radius=18,
            zoom=10,
            height=700
        )

        heatmap_fig.update_layout(
            title='Threat Concentration Heatmap',
            mapbox_style=MAPBOX_STYLE,
            **PLOT_LAYOUT
        )

    else:

        heatmap_fig = empty_threat_fig(
            title='Threat Concentration Heatmap',
            message='No geographic threat data available',
            height=700
        )

    threat_heatmap = heatmap_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # THREAT TIMELINE
    # =====================================

    if (
        not alert_df.empty
        and
        'DATE' in alert_df.columns
        and
        'Crime_Count' in alert_df.columns
    ):

        alert_df = alert_df.dropna(
            subset=[
                'DATE',
                'Crime_Count'
            ]
        )

        if not alert_df.empty:

            timeline_fig = px.line(
                alert_df,
                x='DATE',
                y='Crime_Count',
                markers=True
            )

            timeline_fig.update_traces(
                line=dict(
                    width=4,
                    color='#ef4444'
                )
            )

            timeline_fig.update_layout(
                title='Threat Escalation Timeline',
                height=500,
                hovermode='x unified',
                xaxis_title='Timeline',
                yaxis_title='Escalation Activity',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

        else:

            timeline_fig = empty_threat_fig(
                title='Threat Escalation Timeline',
                message='No threat timeline available'
            )

    else:

        timeline_fig = empty_threat_fig(
            title='Threat Escalation Timeline',
            message='No threat timeline available'
        )

    threat_timeline_graph = timeline_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # THREAT DISTRIBUTION
    # =====================================

    if (
        anomaly_data_available
        and
        'Crime_Count' in anomaly_data.columns
    ):

        anomaly_data = anomaly_data.dropna(
            subset=['Crime_Count']
        )

        if not anomaly_data.empty:

            distribution_fig = px.histogram(
                anomaly_data,
                x='Crime_Count',
                nbins=30,
                color='Anomaly_Label'
            )

            distribution_fig.update_layout(
                title='Threat Distribution Intelligence',
                height=500,
                xaxis_title='Crime Volume',
                yaxis_title='Distribution Density',
                xaxis=AXIS_STYLE,
                yaxis=AXIS_STYLE,
                legend=LEGEND_STYLE,
                **PLOT_LAYOUT
            )

        else:

            distribution_fig = empty_threat_fig(
                title='Threat Distribution Intelligence',
                message='No threat distribution available'
            )

    else:

        distribution_fig = empty_threat_fig(
            title='Threat Distribution Intelligence',
            message='No threat distribution available'
        )

    threat_distribution_graph = distribution_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # THREAT TABLE
    # =====================================

    if (
        not alert_df.empty
        and
        'Crime_Count' in alert_df.columns
    ):

        threat_table = (
            alert_df
            .sort_values(
                by='Crime_Count',
                ascending=False
            )
            .head(20)
            .round(2)
            .to_html(
                classes=TABLE_CLASSES,
                index=False,
                border=0
            )
        )

    else:

        threat_table = """

        <div class="empty-state">

            No threat intelligence available
            for current dataset.

        </div>

        """

    # =====================================
    # RENDER TEMPLATE
    # =====================================

    return render_template(
        "pages/threat_intelligence.html",
        profile=profile,
        anomaly_chart_data=anomaly_chart_data,
        total_alerts=total_alerts,
        highest_risk_zone=highest_risk_zone,
        threat_level=threat_level,
        active_anomalies=active_anomalies,
        monitored_regions=monitored_regions,
        average_threat_score=average_threat_score,
        anomaly_graph=anomaly_graph,
        risk_graph=risk_graph,
        threat_heatmap=threat_heatmap,
        threat_timeline_graph=threat_timeline_graph,
        threat_distribution_graph=threat_distribution_graph,
        threat_table=threat_table
    )