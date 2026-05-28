import pandas as pd

from app import app

from website.models.database import db

from website.models.crime_model import CrimeData

# =====================================
# CSV PATH
# =====================================

CSV_PATH = (

    "D:/FBI_Crime_Project/data/final_cleaned_crime_data.csv"
)

# =====================================
# LOAD CSV
# =====================================

df = pd.read_csv(

    CSV_PATH,

    engine='python',

    on_bad_lines='skip'
)

# =====================================
# IMPORT DATA
# =====================================

with app.app_context():

    # OPTIONAL CLEAR TABLE

    db.session.query(CrimeData).delete()

    db.session.commit()

    # INSERT ROWS

    for _, row in df.iterrows():

        crime = CrimeData(

            year=row.get('YEAR'),

            month=row.get('MONTH'),

            day=row.get('DAY'),

            hour=row.get('HOUR'),

            minute=row.get('MINUTE'),

            neighbourhood=str(
                row.get('NEIGHBOURHOOD')
            ),

            crime_type=str(
                row.get('TYPE')
            ),

            latitude=row.get('Latitude'),

            longitude=row.get('Longitude')
        )

        db.session.add(crime)

    # SAVE

    db.session.commit()

    print(

        "Crime data imported successfully."
    )