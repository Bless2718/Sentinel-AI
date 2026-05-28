from flask import Blueprint, render_template
from flask_login import login_required
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from utils.dataset_profiler import (
    profile_dataset
)

# =====================================
# IMPORT DATA
# =====================================

from utils.data_loader import (
    build_analytics_data,
    PLOT_LAYOUT,
    AXIS_STYLE,
    LEGEND_STYLE,
    TABLE_CLASSES,
    safe_sample
)

# =====================================
# CREATE BLUEPRINT
# =====================================

categories_bp = Blueprint(
    "categories",
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

@categories_bp.route("/crime-categories")
@login_required
def crime_categories():

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

    local_master_df = master_df.copy()

    # =====================================
    # DATASET PROFILE
    # =====================================

    profile = profile_dataset(
        local_master_df
    )

    # =====================================
    # SAFE DATA VALIDATION
    # =====================================

    category_data_available = (

        not local_master_df.empty

        and

        'TYPE'
        in local_master_df.columns
    )

    if category_data_available:

        local_master_df['TYPE'] = (

            local_master_df['TYPE']
            .astype(str)
            .str.strip()
        )

        local_master_df = local_master_df[

            local_master_df['TYPE']
            != ''
        ]

        local_master_df = local_master_df.dropna(
            subset=['TYPE']
        )

        category_data_available = (
            not local_master_df.empty
        )

    # =====================================
    # CATEGORY COUNTS
    # =====================================

    if category_data_available:

        category_counts = (
            local_master_df['TYPE']
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            'Crime_Type',
            'Count'
        ]

        category_counts['Count'] = pd.to_numeric(
            category_counts['Count'],
            errors='coerce'
        )

        category_counts = category_counts.dropna(
            subset=['Count']
        )

    else:

        category_counts = pd.DataFrame(
            columns=[
                'Crime_Type',
                'Count'
            ]
        )

    # =====================================
    # KPI VALUES
    # =====================================

    total_categories = (
        local_master_df['TYPE'].nunique()
        if category_data_available
        else 0
    )

    total_incidents = int(
        category_counts['Count'].sum()
    )

    if not category_counts.empty:

        sorted_categories = (

            category_counts
            .sort_values(
                by='Count',
                ascending=False
            )
        )

        top_crime_type = (
            sorted_categories
            .iloc[0]['Crime_Type']
        )

    else:

        top_crime_type = "UNKNOWN"

    most_dangerous = top_crime_type

    # =====================================
    # PIE CHART
    # =====================================

    if category_data_available and not category_counts.empty:

        pie_fig = px.pie(
            category_counts.head(10),
            names='Crime_Type',
            values='Count',
            hole=0.45
        )

        pie_fig.update_traces(
            textinfo='percent+label',
            textfont=dict(
                color='white',
                size=13
            ),
            hovertemplate=
            '<b>Crime Type:</b> %{label}<br>'
            '<b>Total Incidents:</b> %{value}<br>'
            '<b>Percentage:</b> %{percent}<extra></extra>'
        )

    else:

        pie_fig = go.Figure()

        pie_fig.add_annotation(
            text="No crime category data available",
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

    pie_fig.update_layout(
        title='Crime Category Distribution',
        height=620,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    category_graph = pie_fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config=CHART_CONFIG
    )

    # =====================================
    # TOP CATEGORY GRAPH
    # =====================================

    top_categories = (
        category_counts
        .head(10)
        .sort_values(
            by='Count',
            ascending=True
        )
    )

    if category_data_available and not top_categories.empty:

        bar_fig = px.bar(
            top_categories,
            x='Count',
            y='Crime_Type',
            orientation='h',
            color='Count',
            color_continuous_scale='purples',
            text='Count'
        )

        bar_fig.update_traces(
            textfont=dict(
                color='white',
                size=12
            ),
            hovertemplate=
            '<b>Crime Type:</b> %{y}<br>'
            '<b>Incident Count:</b> %{x}<extra></extra>'
        )

    else:

        bar_fig = go.Figure()

        bar_fig.add_annotation(
            text="No crime category data available",
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

    bar_fig.update_layout(
        title='Top Crime Categories',
        height=620,
        xaxis_title='Incident Count',
        yaxis_title='Crime Category',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
        coloraxis_showscale=False,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    top_category_graph = bar_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # CATEGORY TREND ANALYSIS
    # =====================================

    if (
        category_data_available
        and
        'YEAR' in local_master_df.columns
    ):

        local_master_df['YEAR'] = pd.to_numeric(
            local_master_df['YEAR'],
            errors='coerce'
        )

        yearly_category = (
            local_master_df
            .dropna(subset=['YEAR'])
            .groupby(['YEAR', 'TYPE'])
            .size()
            .reset_index(name='Crime_Count')
        )

        top5 = (
            local_master_df['TYPE']
            .value_counts()
            .head(5)
            .index
        )

        yearly_category = yearly_category[
            yearly_category['TYPE'].isin(top5)
        ]

        if yearly_category.empty:

            trend_fig = go.Figure()

            trend_fig.add_annotation(
                text="No crime category trend data available",
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

        else:

            trend_fig = px.line(
                yearly_category,
                x='YEAR',
                y='Crime_Count',
                color='TYPE',
                markers=True
            )

            trend_fig.update_traces(
                line=dict(
                    width=4
                ),
                marker=dict(
                    size=8
                )
            )

    else:

        trend_fig = go.Figure()

        trend_fig.add_annotation(
            text="No crime category trend data available",
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

    trend_fig.update_layout(
        title='Crime Category Trend Intelligence',
        height=700,
        hovermode='x unified',
        xaxis_title='Year',
        yaxis_title='Crime Activity',
        legend_title='Crime Type',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    trend_graph = trend_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # THREAT ANALYSIS
    # =====================================

    threat_fig = go.Figure()

    if category_data_available and not top_categories.empty:

        top_categories['Count'] = pd.to_numeric(

            top_categories['Count'],

            errors='coerce'
        )

        top_categories = top_categories.dropna(
            subset=['Count']
        )

        if not top_categories.empty:

            threat_fig.add_trace(
                go.Scatter(
                    x=top_categories['Crime_Type'],
                    y=top_categories['Count'],
                    mode='lines+markers',
                    line=dict(
                        color='#ef4444',
                        width=4
                    ),
                    marker=dict(
                        size=10,
                        color='#f87171'
                    ),
                    fill='tozeroy',
                    fillcolor='rgba(239,68,68,0.10)',
                    hovertemplate=
                    '<b>Crime Category:</b> %{x}<br>'
                    '<b>Threat Volume:</b> %{y}<extra></extra>'
                )
            )

        else:

            threat_fig.add_annotation(
                text="No category threat data available",
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

    else:

        threat_fig.add_annotation(
            text="No category threat data available",
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

    threat_fig.update_layout(
        title='Category Threat Analysis',
        height=620,
        hovermode='x unified',
        xaxis_title='Crime Category',
        yaxis_title='Threat Volume',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
        legend=LEGEND_STYLE,
        **PLOT_LAYOUT
    )

    threat_graph = threat_fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=CHART_CONFIG
    )

    # =====================================
    # CATEGORY TABLE
    # =====================================

    if not category_counts.empty:

        category_table = (

            category_counts
            .sort_values(
                by='Count',
                ascending=False
            )
            .to_html(
                classes=TABLE_CLASSES,
                index=False,
                border=0
            )
        )

    else:

        category_table = """

        <div class="empty-state">

            No category intelligence available
            for current dataset.

        </div>

        """

    # =====================================
    # RENDER TEMPLATE
    # =====================================

    return render_template(
        "pages/crime_categories.html",
        profile=profile,
        total_categories=total_categories,
        top_crime_type=top_crime_type,
        most_dangerous=most_dangerous,
        total_incidents=total_incidents,
        category_graph=category_graph,
        top_category_graph=top_category_graph,
        trend_graph=trend_graph,
        threat_graph=threat_graph,
        category_table=category_table
    )