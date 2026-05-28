from flask import Blueprint, jsonify
from website.utils.data_loader import (
    build_analytics_data
)

from website.utils.analytics_engine import (
    calculate_kpis,
    calculate_forecast_metrics
)

from website.utils.risk_engine import (
    calculate_risk_engine
)

from website.utils.alert_engine import (
    generate_operational_alerts
)

from website.utils.intelligence_engine import (
    calculate_crime_volatility
)

# =====================================
# CREATE API BLUEPRINT
# =====================================

api_bp = Blueprint(

    "api",

    __name__
)

# =====================================
# KPI API
# =====================================

@api_bp.route("/api/kpis")
def api_kpis():

    data = build_analytics_data()

    master_df = data['master_df']

    anomaly_df = data['anomaly_df']

    cluster_df = data['cluster_df']

    kpis = calculate_kpis(

        master_df,

        anomaly_df=anomaly_df,

        cluster_df=cluster_df
    )

    return jsonify(

        kpis
    )
    # =====================================
    # APPLY FILTERS
    # =====================================

    filtered_df = apply_dashboard_filters(

        master_df,

        selected_year=selected_year,

        selected_crime=selected_crime,

        selected_threat=selected_threat
    )

    # =====================================
    # KPI ENGINE
    # =====================================

    kpis = calculate_kpis(

        filtered_df,

        anomaly_df=anomaly_df,

        cluster_df=cluster_df
    )

    return jsonify(

        {

            "filters": {

                "year": selected_year,

                "crime": selected_crime,

                "threat": selected_threat
            },

            "results": kpis
        }
    )

# =====================================
# FORECAST API
# =====================================

@api_bp.route("/api/forecast")
def api_forecast():

    data = build_analytics_data()

    forecast_df = data['forecast_df']

    return jsonify(

        forecast_df.tail(30).to_dict(

            orient='records'
        )
    )
# =====================================
# ANOMALY API
# =====================================

@api_bp.route("/api/anomalies")
def api_anomalies():

    data = build_analytics_data()

    anomaly_df = data['anomaly_df']

    return jsonify(

        anomaly_df.to_dict(

            orient='records'
        )
    )

# =====================================
# HOTSPOT API
# =====================================

@api_bp.route("/api/hotspots")
def api_hotspots():

    data = build_analytics_data()

    cluster_df = data['cluster_df']

    return jsonify(

        cluster_df.head(500).to_dict(

            orient='records'
        )
    )
# =====================================
# ALERT API
# =====================================

@api_bp.route("/api/alerts")
def api_alerts():

    data = build_analytics_data()

    master_df = data['master_df']

    forecast_df = data['forecast_df']

    anomaly_df = data['anomaly_df']

    cluster_df = data['cluster_df']

    kpis = calculate_kpis(

        master_df,

        anomaly_df=anomaly_df,

        cluster_df=cluster_df
    )

    forecast_metrics = (

        calculate_forecast_metrics(

            forecast_df
        )
    )

    risk_data = calculate_risk_engine(

        master_df,

        anomaly_df,

        forecast_df,

        cluster_df
    )

    volatility_data = (

        calculate_crime_volatility(

            forecast_df
        )
    )

    alerts = generate_operational_alerts(

        threat_level=kpis['threat_level'],

        risk_score=risk_data['risk_score'],

        anomaly_count=kpis['anomaly_count'],

        active_hotspots=kpis['active_hotspots'],

        forecast_direction=forecast_metrics[
            'forecast_direction'
        ],

        volatility_level=volatility_data[
            'volatility_level'
        ]
    )

    return jsonify(

        alerts
    )