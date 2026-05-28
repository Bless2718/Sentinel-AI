# =====================================
# ALERT ENGINE
# =====================================

def generate_operational_alerts(

    threat_level,
    risk_score,
    anomaly_count,
    active_hotspots,
    forecast_direction,
    volatility_level
):

    alerts = []

    # =====================================
    # THREAT LEVEL ALERTS
    # =====================================

    if threat_level == "CRITICAL":

        alerts.append({

            "title": "Critical Threat Escalation",

            "message": (
                "Operational threat level "
                "has reached CRITICAL status."
            ),

            "severity": "critical"
        })

    elif threat_level == "HIGH":

        alerts.append({

            "title": "High Threat Activity",

            "message": (
                "Elevated threat activity "
                "detected across monitored regions."
            ),

            "severity": "high"
        })

    # =====================================
    # RISK SCORE ALERT
    # =====================================

    if risk_score >= 80:

        alerts.append({

            "title": "Extreme Risk Score",

            "message": (
                f"Risk score escalated "
                f"to {risk_score}%."
            ),

            "severity": "critical"
        })

    # =====================================
    # ANOMALY ALERT
    # =====================================

    if anomaly_count >= 10:

        alerts.append({

            "title": "Anomaly Spike Detected",

            "message": (
                f"{anomaly_count} anomaly events "
                "identified by AI systems."
            ),

            "severity": "high"
        })

    # =====================================
    # HOTSPOT ALERT
    # =====================================

    if active_hotspots >= 5:

        alerts.append({

            "title": "Hotspot Escalation",

            "message": (
                f"{active_hotspots} active "
                "crime hotspots under surveillance."
            ),

            "severity": "moderate"
        })

    # =====================================
    # FORECAST ALERT
    # =====================================

    if forecast_direction == "ESCALATING":

        alerts.append({

            "title": "Forecast Escalation",

            "message": (
                "Predictive forecasting indicates "
                "rising crime activity."
            ),

            "severity": "high"
        })

    # =====================================
    # VOLATILITY ALERT
    # =====================================

    if volatility_level == "HIGH":

        alerts.append({

            "title": "Forecast Volatility Warning",

            "message": (
                "High forecasting volatility "
                "detected in predictive systems."
            ),

            "severity": "moderate"
        })

    # =====================================
    # DEFAULT ALERT
    # =====================================

    if len(alerts) == 0:

        alerts.append({

            "title": "Systems Stable",

            "message": (
                "No major operational threats "
                "detected."
            ),

            "severity": "low"
        })

    return alerts