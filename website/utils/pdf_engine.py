from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

# =====================================
# PDF ENGINE
# =====================================

def generate_intelligence_pdf(

    output_path,

    kpis,

    alerts,

    strategic_report
):

    # =====================================
    # PDF DOCUMENT
    # =====================================

    doc = SimpleDocTemplate(

        output_path,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # =====================================
    # TITLE
    # =====================================

    elements.append(

        Paragraph(

            "Sentinel AI Intelligence Report",

            styles['Title']
        )
    )

    elements.append(

        Spacer(1, 20)
    )

    # =====================================
    # KPI SECTION
    # =====================================

    elements.append(

        Paragraph(

            "Operational KPIs",

            styles['Heading2']
        )
    )

    for key, value in kpis.items():

        elements.append(

            Paragraph(

                f"<b>{key}</b>: {value}",

                styles['BodyText']
            )
        )

    elements.append(

        Spacer(1, 20)
    )

    # =====================================
    # ALERT SECTION
    # =====================================

    elements.append(

        Paragraph(

            "Operational Alerts",

            styles['Heading2']
        )
    )

    for alert in alerts:

        elements.append(

            Paragraph(

                (
                    f"<b>{alert['title']}</b>: "
                    f"{alert['message']}"
                ),

                styles['BodyText']
            )
        )

    elements.append(

        Spacer(1, 20)
    )

    # =====================================
    # STRATEGIC REPORT
    # =====================================

    elements.append(

        Paragraph(

            "Strategic Intelligence Summary",

            styles['Heading2']
        )
    )

    elements.append(

        Paragraph(

            strategic_report.replace(
                "\n",
                "<br/>"
            ),

            styles['BodyText']
        )
    )

    # =====================================
    # BUILD PDF
    # =====================================

    doc.build(elements)