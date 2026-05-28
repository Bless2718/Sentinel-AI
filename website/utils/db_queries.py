import pandas as pd

from models.crime_model import CrimeData

# =====================================
# THREAT CLASSIFICATION ENGINE
# =====================================

HIGH_THREAT_CRIMES = [

    'HOMICIDE',
    'ROBBERY',
    'ASSAULT',
    'SHOOTING',
    'KIDNAPPING',
    'WEAPON'
]

MODERATE_THREAT_CRIMES = [

    'BURGLARY',
    'AUTO THEFT',
    'BREAK AND ENTER',
    'FRAUD'
]

# =====================================
# CLASSIFY THREAT LEVEL
# =====================================

def classify_threat(crime_type):

    if not crime_type:

        return 'LOW'

    crime_type = str(crime_type).upper()

    # HIGH

    if any(

        keyword in crime_type

        for keyword in HIGH_THREAT_CRIMES
    ):

        return 'HIGH'

    # MODERATE

    if any(

        keyword in crime_type

        for keyword in MODERATE_THREAT_CRIMES
    ):

        return 'MODERATE'

    # DEFAULT

    return 'LOW'

# =====================================
# LOAD CRIME DATAFRAME
# =====================================

def load_crime_dataframe():

    try:

        crimes = CrimeData.query.all()

        # =====================================
        # EMPTY SAFETY
        # =====================================

        if not crimes:

            return pd.DataFrame(columns=[

                'YEAR',
                'MONTH',
                'DAY',
                'HOUR',
                'MINUTE',
                'DATE',
                'TYPE',
                'NEIGHBOURHOOD',
                'Latitude',
                'Longitude',
                'THREAT_LEVEL'
            ])

        # =====================================
        # CONVERT TO DICTIONARY
        # =====================================

        data = []

        for crime in crimes:

            data.append({

                'YEAR': crime.year,

                'MONTH': crime.month,

                'DAY': crime.day,

                'HOUR': crime.hour,

                'MINUTE': crime.minute,

                'TYPE': crime.crime_type,

                'NEIGHBOURHOOD': crime.neighbourhood,

                'Latitude': crime.latitude,

                'Longitude': crime.longitude
            })

        # =====================================
        # CREATE DATAFRAME
        # =====================================

        df = pd.DataFrame(data)

        # =====================================
        # ENSURE REQUIRED COLUMNS
        # =====================================

        required_columns = [

            'YEAR',
            'MONTH',
            'DAY',
            'HOUR',
            'MINUTE',
            'TYPE',
            'NEIGHBOURHOOD',
            'Latitude',
            'Longitude'
        ]

        for column in required_columns:

            if column not in df.columns:

                df[column] = None

        # =====================================
        # CLEAN NUMERIC COLUMNS
        # =====================================

        numeric_columns = [

            'YEAR',
            'MONTH',
            'DAY',
            'HOUR',
            'MINUTE',
            'Latitude',
            'Longitude'
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(

                df[column],

                errors='coerce'
            )

        # =====================================
        # CLEAN TEXT COLUMNS
        # =====================================

        df['TYPE'] = (

            df['TYPE']
            .fillna('UNKNOWN')
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df['NEIGHBOURHOOD'] = (

            df['NEIGHBOURHOOD']
            .fillna('UNKNOWN')
            .astype(str)
            .str.title()
            .str.strip()
        )

        # =====================================
        # CREATE DATE COLUMN
        # =====================================

        df['DATE'] = pd.to_datetime(

            dict(

                year=df['YEAR'].fillna(2024),

                month=df['MONTH'].fillna(1),

                day=df['DAY'].fillna(1)
            ),

            errors='coerce'
        )

        # =====================================
        # REMOVE INVALID DATES
        # =====================================

        df = df.dropna(

            subset=['DATE']
        )

        # =====================================
        # THREAT LEVEL ENGINE
        # =====================================

        df['THREAT_LEVEL'] = (

            df['TYPE']
            .apply(classify_threat)
        )

        # =====================================
        # RESET INDEX
        # =====================================

        df.reset_index(

            drop=True,

            inplace=True
        )

        return df

    except Exception as e:

        print(

            f"LOAD CRIME DATAFRAME ERROR: {e}"
        )

        return pd.DataFrame(columns=[

            'YEAR',
            'MONTH',
            'DAY',
            'HOUR',
            'MINUTE',
            'DATE',
            'TYPE',
            'NEIGHBOURHOOD',
            'Latitude',
            'Longitude',
            'THREAT_LEVEL'
        ])