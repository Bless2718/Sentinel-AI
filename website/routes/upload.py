from website.utils.data_registry import (
    ACTIVE_DATA
)
from website.utils.data_loader import (
    build_analytics_data
)
from website.utils.ai_pipeline import (
    generate_forecast,
    generate_anomalies,
    generate_hotspots
)
from flask_login import login_required
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from website.utils.data_standardizer import (
    standardize_dataframe
)

import pandas as pd

from pathlib import Path

# =====================================
# BLUEPRINT
# =====================================

upload_bp = Blueprint(
    "upload",
    __name__
)

# =====================================
# UPLOAD FOLDER
# =====================================

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
    )
# =====================================
# GLOBAL STORAGE
# =====================================

uploaded_data = {}

# =====================================
# UPLOAD PAGE
# =====================================

@upload_bp.route("/upload")
@login_required
def upload_page():

    return render_template(
        "pages/upload.html"
    )

# =====================================
# HANDLE FILE UPLOAD
# =====================================

@upload_bp.route(
    "/upload-data",
    methods=["POST"]
)
@login_required
def upload_data():

    global uploaded_data

    if 'dataset' not in request.files:

        flash(
            "No file selected.",
            "danger"
        )

        return redirect(
            url_for("upload.upload_page")
        )

    file = request.files['dataset']

    if file.filename == '':

        flash(
            "No file selected.",
            "danger"
        )

        return redirect(
            url_for("upload.upload_page")
        )

    try:

        save_path = (
            UPLOAD_FOLDER / file.filename
        )

        file.save(save_path)

        # =====================================
        # READ FILE
        # =====================================

        if file.filename.endswith(".csv"):

            uploaded_data['data'] = pd.read_csv(
                save_path,
                encoding='latin1',
                low_memory=False
            )

            uploaded_data['data'] = standardize_dataframe(
                uploaded_data['data']
            )

        elif file.filename.endswith((".xlsx", ".xls")):

            uploaded_data['data'] = pd.read_excel(
                save_path
            )

            uploaded_data['data'] = standardize_dataframe(
                uploaded_data['data']
            )

        else:

            flash(
                "Unsupported file type.",
                "danger"
            )

            return redirect(
                url_for("upload.upload_page")
            )

        # =====================================
        # GENERATE AI OUTPUTS
        # =====================================

        uploaded_data['forecast_df'] = (
            generate_forecast(
                uploaded_data['data']
            )
        )

        uploaded_data['anomaly_df'] = (
            generate_anomalies(
                uploaded_data['data']
            )
        )

        uploaded_data['cluster_df'] = (
            generate_hotspots(
                uploaded_data['data']
            )
        )
        # =====================================
# REPLACE ACTIVE DATASET
# =====================================
        ACTIVE_DATA['master_df'] = (
            uploaded_data['data']
        )
        ACTIVE_DATA['forecast_df'] = (
            uploaded_data['forecast_df']
        )
        ACTIVE_DATA['anomaly_df'] = (
            uploaded_data['anomaly_df']
        )
        ACTIVE_DATA['cluster_df'] = (
            uploaded_data['cluster_df']
        )
        ACTIVE_DATA['risk_df'] = pd.DataFrame()
        # =====================================
# REFRESH ANALYTICS CACHE
# =====================================
        
        # =====================================
        # SUCCESS
        # =====================================

        flash(
            f"Dataset uploaded successfully. Rows loaded: {len(uploaded_data['data'])}",
            "success"
        )

        return redirect("/")

    except Exception as e:

        print("\nUPLOAD ERROR:\n")

        print(str(e))

        print("\n")

        raise e