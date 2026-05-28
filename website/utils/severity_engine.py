# =====================================
# CRIME SEVERITY ENGINE
# =====================================

CRIME_SEVERITY = {

    "HOMICIDE": 10,
    "MURDER": 10,

    "ROBBERY": 8,

    "ASSAULT": 7,
    "AGGRAVATED ASSAULT": 8,

    "BURGLARY": 6,

    "FRAUD": 5,
    "AUTO THEFT": 5,
    "VEHICLE THEFT": 5,

    "THEFT": 4,
    "SHOPLIFTING": 3,

    "VANDALISM": 3,

    "DISORDERLY CONDUCT": 2
}

# =====================================
# GET SINGLE CRIME SEVERITY
# =====================================

def get_crime_severity(crime_type):

    if not crime_type:

        return 1

    return CRIME_SEVERITY.get(

        str(crime_type).upper(),

        3
    )

# =====================================
# CALCULATE DATAFRAME SEVERITY
# =====================================

def calculate_dataframe_severity(df):

    if df.empty:

        return 0

    if 'TYPE' not in df.columns:

        return 0

    total_score = 0

    for crime in df['TYPE']:

        total_score += get_crime_severity(

            crime
        )

    return total_score

# =====================================
# ADD SEVERITY COLUMN
# =====================================

def add_severity_column(df):

    if df.empty:

        return df

    if 'TYPE' not in df.columns:

        return df

    df = df.copy()

    df['SEVERITY_SCORE'] = df['TYPE'].apply(

        get_crime_severity
    )

    return df