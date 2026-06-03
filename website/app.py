from website.utils.data_loader import build_analytics_data
from flask import Flask
import os
from website.models.user_model import User
from flask_login import LoginManager
from website.routes.auth import auth_bp
from website.routes.api.api_routes import (
    api_bp
)
# =====================================
# DATABASE
# =====================================

from website.models.database import db

# =====================================
# CREATE FLASK APP
# =====================================

app = Flask(__name__)
# =====================================
# GLOBAL ANALYTICS CACHE
# =====================================


# =====================================
# BASE DIRECTORY
# =====================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

# =====================================
# DATABASE PATH
# =====================================

db_path = os.path.join(
    BASE_DIR,
    "crime_intelligence.db"
)

# =====================================
# APPLICATION CONFIGURATION
# =====================================

app.config.update(

    SECRET_KEY="sentinel-ai-secure-key",

    SQLALCHEMY_DATABASE_URI=(
        f"sqlite:///{db_path}"
    ),

    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    TEMPLATES_AUTO_RELOAD=True,

    JSON_SORT_KEYS=False
)

# =====================================
# INITIALIZE DATABASE
# =====================================

db.init_app(app)
# =====================================
# LOGIN MANAGER
# =====================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"
# =====================================
# LOAD USER
# =====================================
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
    User,
    int(user_id)
)
# =====================================
# import website.models
# =====================================

from website.models.crime_model import CrimeData

# =====================================
# IMPORT BLUEPRINTS
# =====================================

from website.routes.home import home_bp

from website.routes.forecasting import forecasting_bp

from website.routes.geographic import geographic_bp

from website.routes.categories import categories_bp

from website.routes.time_intelligence import time_bp

from website.routes.threat import threat_bp

from website.routes.upload import upload_bp

# =====================================
# REGISTER BLUEPRINTS
# =====================================

BLUEPRINTS = [

    home_bp,

    forecasting_bp,

    geographic_bp,

    categories_bp,

    time_bp,

    threat_bp,

    upload_bp
]

for blueprint in BLUEPRINTS:

    app.register_blueprint(
        blueprint
    )

# =====================================
# GLOBAL TEMPLATE VARIABLES
# =====================================

@app.context_processor
def inject_global_variables():

    return dict(

        dashboard_name="Sentinel AI",

        dashboard_version="v3.0",

        organization="FBI Crime Forecast System"
    )

# =====================================
# HOME TEST ROUTE
# =====================================

@app.route("/health")
def health_check():

    return {

        "status": "online",

        "platform": "Sentinel AI",

        "version": "3.0"
    }

# =====================================
# DATABASE TEST ROUTE
# =====================================

@app.route("/db-check")
def db_check():

    total_records = CrimeData.query.count()

    return {

        "database": "connected",

        "records": total_records
    }

# =====================================
# ERROR HANDLER - 404
# =====================================

@app.errorhandler(404)
def page_not_found(error):

    return (

        """
        <body style="
            background:#020617;
            color:white;
            font-family:Inter,sans-serif;
            padding:40px;
        ">

            <h1>404 | Page Not Found</h1>

            <p>
                The requested intelligence route
                could not be located.
            </p>

        </body>
        """,

        404
    )

# =====================================
# ERROR HANDLER - 500
# =====================================

@app.errorhandler(500)
def internal_error(error):

    return (

        f"""
        <body style="
            background:#020617;
            color:white;
            font-family:Inter,sans-serif;
            padding:40px;
        ">

            <h1>500 | Internal Server Error</h1>

            <p>
                Sentinel AI encountered an
                unexpected processing error.
            </p>

            <pre>
{error}
            </pre>

        </body>
        """,

        500
    )

# =====================================
# CREATE DATABASE TABLES
# =====================================

with app.app_context():

    db.create_all()

# =====================================
# RUN APPLICATION
# =====================================
with app.app_context():

    db.create_all()
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )