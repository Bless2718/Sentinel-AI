import pandas as pd

# =====================================
# APPLY SMART FILTERS
# =====================================

def apply_dashboard_filters(

    df,
    year='ALL',
    crime='ALL',
    threat='ALL'
):

    """
    Centralized dashboard filtering engine.
    """

    # =====================================
    # EMPTY SAFETY
    # =====================================

    if df.empty:

        return df

    # =====================================
    # COPY DATAFRAME
    # =====================================

    filtered_df = df.copy()

    # =====================================
    # CLEAN COLUMNS
    # =====================================

    if 'YEAR' in filtered_df.columns:

        filtered_df['YEAR'] = pd.to_numeric(

            filtered_df['YEAR'],

            errors='coerce'
        )

    if 'TYPE' in filtered_df.columns:

        filtered_df['TYPE'] = (

            filtered_df['TYPE']
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # =====================================
    # SYNTHETIC THREAT ENGINE
    # =====================================

    if 'TYPE' in filtered_df.columns:

        filtered_df['THREAT_LEVEL'] = (

            filtered_df['TYPE']
            .apply(

                lambda x:

                'CRITICAL'

                if x in [

                    'HOMICIDE',
                    'MURDER'
                ]

                else (

                    'HIGH'

                    if x in [

                        'ROBBERY',
                        'ASSAULT',
                        'WEAPONS'
                    ]

                    else (

                        'MODERATE'

                        if x in [

                            'BURGLARY',
                            'AUTO THEFT'
                        ]

                        else 'LOW'
                    )
                )
            )
        )

    # =====================================
    # YEAR FILTER
    # =====================================

    if (

        year not in [

            'ALL',
            '',
            None
        ]

        and

        'YEAR' in filtered_df.columns
    ):

        filtered_df = filtered_df[

            filtered_df['YEAR']
            .astype(str)

            ==

            str(year)
        ]

    # =====================================
    # CRIME FILTER
    # =====================================

    if (

        crime not in [

            'ALL',
            '',
            None
        ]

        and

        'TYPE' in filtered_df.columns
    ):

        filtered_df = filtered_df[

            filtered_df['TYPE']

            ==

            str(crime).upper()
        ]

    # =====================================
    # THREAT FILTER
    # =====================================

    if (

        threat not in [

            'ALL',
            '',
            None
        ]

        and

        'THREAT_LEVEL' in filtered_df.columns
    ):

        filtered_df = filtered_df[

            filtered_df['THREAT_LEVEL']

            ==

            str(threat).upper()
        ]

    return filtered_df