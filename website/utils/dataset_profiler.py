import pandas as pd

# =====================================
# SEMANTIC COLUMN GROUPS
# =====================================

COLUMN_PATTERNS = {

    "DATE": [

        "date",
        "timestamp",
        "occurred",
        "incident_date",
        "reported_date",
        "datetime",
        "time"
    ],

    "TYPE": [

        "type",
        "crime",
        "offense",
        "offense_group",
        "incident",
        "category",
        "primary_type"
    ],

    "LATITUDE": [

        "lat",
        "latitude",
        "y_coord",
        "y"
    ],

    "LONGITUDE": [

        "lon",
        "lng",
        "longitude",
        "x_coord",
        "x"
    ],

    "NEIGHBORHOOD": [

        "district",
        "neighborhood",
        "area",
        "zone",
        "region",
        "precinct"
    ],

    "HOUR": [

        "hour",
        "time_hour"
    ]
}

# =====================================
# DETECT COLUMN
# =====================================

def detect_column(df, patterns):

    for column in df.columns:

        column_lower = str(column).lower()

        for pattern in patterns:

            if pattern in column_lower:

                return column

    return None

# =====================================
# PROFILE DATASET
# =====================================

def profile_dataset(df):

    profile = {}

    # =====================================
    # DETECT CORE COLUMNS
    # =====================================

    detected_columns = {}

    for standard_name, patterns in COLUMN_PATTERNS.items():

        detected_columns[standard_name] = (

            detect_column(df, patterns)
        )

    profile['columns'] = detected_columns

    # =====================================
    # CAPABILITIES
    # =====================================

    profile['supports_forecasting'] = (

        detected_columns['DATE'] is not None
    )

    profile['supports_hotspots'] = (

        detected_columns['LATITUDE'] is not None
        and
        detected_columns['LONGITUDE'] is not None
    )

    profile['supports_category_analysis'] = (

        detected_columns['TYPE'] is not None
    )

    profile['supports_time_analysis'] = (

        detected_columns['DATE'] is not None
        or
        detected_columns['HOUR'] is not None
    )

    profile['supports_geographic_analysis'] = (

        detected_columns['LATITUDE'] is not None
        and
        detected_columns['LONGITUDE'] is not None
    )

    # =====================================
    # DATA HEALTH
    # =====================================

    profile['row_count'] = len(df)

    profile['column_count'] = len(df.columns)

    profile['missing_values'] = int(

        df.isna().sum().sum()
    )

    return profile