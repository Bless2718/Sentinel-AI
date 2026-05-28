from app import app

from models.database import db

# IMPORT YOUR MODEL
from models.crime_model import CrimeData

with app.app_context():

    # OPTIONAL:
    # clears old broken tables

    db.drop_all()

    # create fresh tables

    db.create_all()

    print(
        "Database tables created successfully."
    )