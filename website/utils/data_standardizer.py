import pandas as pd

from utils.dataset_profiler import (
    profile_dataset
)

# =====================================
# STANDARDIZE DATAFRAME
# =====================================

def standardize_dataframe(df):

    print("\n========= RAW DATASET COLUMNS =========")
    print(df.columns.tolist())
    print("=======================================\n")

    # =====================================
    # PROFILE DATASET
    # =====================================

    profile = profile_dataset(df)
    # =====================================
# SAFE COPY
# =====================================

    df = df.copy()

# =====================================
# NORMALIZE COLUMN NAMES
# =====================================

    df.columns = [

        str(col).strip()

        for col in df.columns
]
    detected = profile['columns']

    
    
    # =====================================
    # CREATE STANDARDIZED DF
    # =====================================

    standardized = df.copy()

    # =====================================
    # CRIME TYPE DETECTION
    # =====================================

    crime_type_candidates = [

        'TYPE',

        'OFFENSE_CODE_GROUP',

        'OFFENSE_DESCRIPTION',

        'Crime_Type',

        'CRIME_TYPE',

        'CATEGORY',

        'OFFENSE',

        'OFFENCE',

        'CRIME',

        'DESCRIPTION',

        'Primary Type',

        'EVENT_TYPE'
    ]

    type_found = False

    for col in crime_type_candidates:

        if col in df.columns:

            print(f"\nTYPE MAPPED FROM: {col}\n")

            standardized['TYPE'] = (

                df[col]
                .astype(str)
                .str.strip()
            )

            type_found = True

            break

    # =====================================
    # FALLBACK TYPE
    # =====================================

    if not type_found:

        standardized['TYPE'] = "UNKNOWN"

    # =====================================
    # CLEAN TYPE VALUES
    # =====================================

    standardized['TYPE'] = (

        standardized['TYPE']
        .astype(str)
        .str.strip()
    )
    standardized.loc[
        standardized['TYPE'].isin(
             ['', 'nan', 'None']
             ),
             'TYPE'
    ] = "UNKNOWN"

    # =====================================
    # NEIGHBOURHOOD DETECTION
    # =====================================

    neighborhood_candidates = [

        'NEIGHBOURHOOD',

        'NEIGHBORHOOD',

        'DISTRICT',

        'AREA',

        'PRECINCT',

        'SECTOR',

        'ZONE',

        'COMMUNITY'
    ]

    neighborhood_found = False

    for col in neighborhood_candidates:

        if col in df.columns:

            standardized['NEIGHBOURHOOD'] = (

                df[col]
                .astype(str)
                .str.strip()
            )

            neighborhood_found = True

            break

    if not neighborhood_found:

        standardized['NEIGHBOURHOOD'] = "UNKNOWN"

    # =====================================
    # DATE DETECTION
    # =====================================

    date_candidates = [

        'DATE',

        'Date',

        'OCCURRED_ON_DATE',

        'EVENT_DATE',

        'TIMESTAMP',

        'Reported_Date'
    ]

    for col in date_candidates:

        if col in df.columns:

            standardized['DATE'] = pd.to_datetime(

                df[col],

                errors='coerce'
            )

            break

    # =====================================
    # YEAR DETECTION
    # =====================================

    if 'YEAR' in df.columns:

        standardized['YEAR'] = pd.to_numeric(

            df['YEAR'],

            errors='coerce'
        )

    elif 'DATE' in standardized.columns:

        standardized['YEAR'] = (

            standardized['DATE']
            .dt.year
        )

    # =====================================
    # MONTH DETECTION
    # =====================================

    if 'MONTH' in df.columns:

        standardized['MONTH'] = pd.to_numeric(

            df['MONTH'],

            errors='coerce'
        )

    elif 'DATE' in standardized.columns:

        standardized['MONTH'] = (

            standardized['DATE']
            .dt.month
        )

    # =====================================
    # DAY DETECTION
    # =====================================

    if 'DAY' in df.columns:

        standardized['DAY'] = pd.to_numeric(

            df['DAY'],

            errors='coerce'
        )

    elif 'DATE' in standardized.columns:

        standardized['DAY'] = (

            standardized['DATE']
            .dt.day
        )

    # =====================================
    # HOUR DETECTION
    # =====================================

    if 'HOUR' in df.columns:

        standardized['HOUR'] = pd.to_numeric(

            df['HOUR'],

            errors='coerce'
        )

    elif 'DATE' in standardized.columns:

        standardized['HOUR'] = (

            standardized['DATE']
            .dt.hour
        )

    # =====================================
    # MINUTE DETECTION
    # =====================================

    if 'MINUTE' in df.columns:

        standardized['MINUTE'] = pd.to_numeric(

            df['MINUTE'],

            errors='coerce'
        )

    # =====================================
    # LATITUDE DETECTION
    # =====================================

    latitude_candidates = [

        'Latitude',

        'LATITUDE',

        'Lat',

        'LAT'
    ]

    for col in latitude_candidates:

        if col in df.columns:

            standardized['Latitude'] = pd.to_numeric(

                df[col],

                errors='coerce'
            )

            break

    # =====================================
    # LONGITUDE DETECTION
    # =====================================

    longitude_candidates = [

        'Longitude',

        'LONGITUDE',

        'Long',

        'LON'
    ]

    for col in longitude_candidates:

        if col in df.columns:

            standardized['Longitude'] = pd.to_numeric(

                df[col],

                errors='coerce'
            )

            break

    # =====================================
    # HUNDRED BLOCK
    # =====================================

    if 'HUNDRED_BLOCK' in df.columns:

        standardized['HUNDRED_BLOCK'] = (

            df['HUNDRED_BLOCK']
            .astype(str)
        )

    
    # =====================================
    # CRIME COUNT
    # =====================================

    standardized['Crime_Count'] = 1

    # =====================================
    # RESET INDEX
    # =====================================

    standardized = standardized.reset_index(
        drop=True
    )

    # =====================================
    # DEBUG OUTPUT
    # =====================================

    print("\n========= STANDARDIZED COLUMNS =========")
    print(standardized.columns.tolist())
    print("========================================\n")

    print("\n========= TYPE SAMPLE =========")
    print(standardized['TYPE'].head())
    print("================================\n")

    print("\n========= DATA SAMPLE =========")
    print(standardized.head())
    print("================================\n")

    return standardized