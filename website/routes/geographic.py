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

geographic_bp = Blueprint(
    "geographic",
    __name__
)

# =====================================
# CHART CONFIG
# =====================================

CHART_CONFIG = dict(
    displayModeBar=False,
    responsive=True
)

# =====================================
# ROUTE
# =====================================

@geographic_bp.route("/geographic")
@login_required
def geographic():

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
    # LOCAL DATA COPY
    # =====================================

    local_cluster_df = cluster_df.copy()

    local_risk_df = risk_df.copy()

    # =====================================
    # DATASET PROFILE
    # =====================================

    profile = profile_dataset(
        master_df
    )

    # =====================================
    # SAFE HOTSPOT VALIDATION
    # =====================================

    hotspot_data_available = (

        not local_cluster_df.empty

        and

        'Latitude'
        in local_cluster_df.columns

        and

        'Longitude'
        in local_cluster_df.columns

        and

        'Cluster'
        in local_cluster_df.columns
    )

    if hotspot_data_available:

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

        # REMOVE INVALID COORDINATES

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

        hotspot_data_available = (
            not local_cluster_df.empty
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
    # SAFE RISK DATA VALIDATION
    # =====================================

    risk_data_available = (
        not local_risk_df.empty
        and
        'Cluster_Name' in local_risk_df.columns
        and
        'Risk_Score' in local_risk_df.columns
    )

    # =====================================
    # SAFE SAMPLE
    # =====================================

    if hotspot_data_available:

        hotspot_sample = safe_sample(
            local_cluster_df,
            6000
        )

    else:

        hotspot_sample = pd.DataFrame()

    if hotspot_sample.empty:

        hotspot_data_available = False

    # =====================================
    # KPI VALUES
    # =====================================

    active_hotspots = (
        hotspot_sample['Cluster'].nunique()
        if hotspot_data_available
        else 0
    )

    high_risk_zones = (
        local_risk_df[
            local_risk_df['Risk_Level'] == 'HIGH'
        ].shape[0]
        if 'Risk_Level' in local_risk_df.columns
        else 0
    )

    threat_density = (
        "HIGH"
        if high_risk_zones >= 3
        else "MEDIUM"
        if high_risk_zones >= 1
        else "LOW"
    )

    cluster_regions = (
        hotspot_sample['Cluster'].nunique()
        if hotspot_data_available
        else 0
    )

    # =====================================
    # HOTSPOT MAP
    # =====================================

    if hotspot_data_available:

        map_fig = px.scatter_map(
            hotspot_sample,
            lat='Latitude',
            lon='Longitude',
            color='Cluster',
            hover_data=[
                'Cluster'
            ],
            zoom=9,
            height=750
        )

    else:

        map_fig = go.Figure()

        map_fig.add_annotation(
            text="No geographic hotspot intelligence available",
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

    if hotspot_data_available:

        map_fig.update_traces(

            marker=dict(
                size=9,
                opacity=0.82
            )
        )

    map_fig.update_layout(
        title='Crime Hotspot Intelligence',
        height=750,
        mapbox_style=MAPBOX_STYLE,
        hovermode='closest',
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    hotspot_map = map_fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config=CHART_CONFIG
    )

    # =====================================
    # HEATMAP
    # =====================================

    if hotspot_data_available:

        heatmap_fig = px.density_map(
            hotspot_sample,
            lat='Latitude',
            lon='Longitude',
            radius=14,
            zoom=9,
            height=700
        )

    else:

        heatmap_fig = go.Figure()

        heatmap_fig.add_annotation(
            text="No geographic hotspot intelligence available",
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

    heatmap_fig.update_layout(
        title='Crime Density Heatmap',
        height=700,
        mapbox_style=MAPBOX_STYLE,
        **PLOT_LAYOUT
    )

    heatmap_graph = heatmap_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # RISK SCORE CHART
    # =====================================

    if risk_data_available:

        risk_chart = px.bar(
            local_risk_df,
            x='Cluster_Name',
            y='Risk_Score',
            color='Risk_Score',
            height=500
        )

    else:

        risk_chart = go.Figure()

        risk_chart.add_annotation(
            text="No risk intelligence data available",
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

    risk_chart.update_layout(
        title='Geographic Risk Intelligence',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    risk_chart_html = risk_chart.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # RISK TABLE
    # =====================================

    if not local_risk_df.empty:

        risk_table = (

            local_risk_df
            .round(2)
            .to_html(

                classes=TABLE_CLASSES,

                index=False,

                border=0
            )
        )

    else:

        risk_table = """

        <div class="empty-state">

            No geographic risk intelligence
            available for current dataset.

        </div>

        """

    # =====================================
    # GEOSPATIAL INSIGHTS
    # =====================================

    if (

        risk_data_available

        and

        not local_risk_df.empty

        and

        'Cluster_Name'
        in local_risk_df.columns
    ):

        sorted_risk_df = local_risk_df.sort_values(

            by='Risk_Score',

            ascending=False
        )

        if not sorted_risk_df.empty:

            highest_cluster = (
                sorted_risk_df.iloc[0]['Cluster_Name']
            )

        else:

            highest_cluster = "UNKNOWN"

    else:

        highest_cluster = "UNKNOWN"

    # =====================================
    # RENDER TEMPLATE
    # =====================================

    return render_template(
        "pages/geographic.html",
        profile=profile,
        active_hotspots=active_hotspots,
        high_risk_zones=high_risk_zones,
        threat_density=threat_density,
        cluster_regions=cluster_regions,
        hotspot_map=hotspot_map,
        heatmap_graph=heatmap_graph,
        risk_graph=risk_chart_html,
        risk_table=risk_table,
        highest_cluster=highest_cluster
    )