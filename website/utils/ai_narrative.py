# =====================================
# HUMAN AI NARRATIVE ENGINE
# =====================================

def generate_ai_narrative(

    threat_level,
    forecast_direction,
    anomaly_count,
    active_hotspots,
    ai_confidence,
    latest_forecast
):

    insights = []

    # =====================================
    # THREAT ANALYSIS
    # =====================================

    if threat_level == "CRITICAL":

        insights.append(

            "Crime activity is currently at a critical level. "
            "Several unusual patterns were detected across monitored regions, "
            "which may require immediate attention from operational teams."
        )

    elif threat_level == "HIGH":

        insights.append(

            "Crime activity is higher than normal in multiple areas. "
            "The system detected an increase in suspicious or abnormal activity "
            "that should continue to be monitored closely."
        )

    elif threat_level == "MODERATE":

        insights.append(

            "Current crime activity remains moderately elevated. "
            "While the situation is stable overall, a few regions are showing "
            "early signs of increased activity."
        )

    else:

        insights.append(

            "Crime activity is currently stable across most monitored areas. "
            "No major escalation patterns were detected at this time."
        )

    # =====================================
    # FORECAST ANALYSIS
    # =====================================

    if forecast_direction == "ESCALATING":

        insights.append(

            f"The forecasting system predicts a gradual increase in crime activity. "
            f"Current projections estimate future activity levels reaching approximately "
            f"{latest_forecast:.0f} incidents during upcoming monitoring periods."
        )

    elif forecast_direction == "DECLINING":

        insights.append(

            "Forecast models indicate that crime activity may slowly decrease "
            "over the upcoming monitoring periods."
        )

    else:

        insights.append(

            "Forecast patterns currently appear stable with no major upward "
            "or downward movement expected."
        )

    # =====================================
    # HOTSPOT ANALYSIS
    # =====================================

    if active_hotspots >= 10:

        insights.append(

            "A large number of geographic hotspot zones are currently active. "
            "This suggests crime activity is spreading across multiple regions."
        )

    elif active_hotspots >= 5:

        insights.append(

            "Several active hotspot regions were identified by the AI system. "
            "These areas may require additional monitoring and resource allocation."
        )

    else:

        insights.append(

            "Only a small number of hotspot regions are currently active, "
            "indicating localized crime concentration."
        )

    # =====================================
    # ANOMALY ANALYSIS
    # =====================================

    if anomaly_count >= 15:

        insights.append(

            "The anomaly detection engine identified a high number of unusual "
            "activity patterns. This may indicate emerging operational risks."
        )

    elif anomaly_count >= 5:

        insights.append(

            "A moderate number of unusual activity events were detected. "
            "These incidents should continue to be monitored over time."
        )

    else:

        insights.append(

            "Very few unusual incidents were detected during the latest analysis cycle."
        )

    # =====================================
    # AI CONFIDENCE
    # =====================================

    if ai_confidence >= 90:

        insights.append(

            "The AI system currently has a very high confidence level in its "
            "forecasting and anomaly detection results."
        )

    elif ai_confidence >= 75:

        insights.append(

            "The AI system confidence level remains stable and suitable for "
            "operational monitoring."
        )

    else:

        insights.append(

            "AI confidence levels are lower than expected. "
            "Additional data may improve prediction reliability."
        )

    return insights