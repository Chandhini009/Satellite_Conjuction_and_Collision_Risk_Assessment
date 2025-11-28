# Connect 01_EDA.ipynb

import pandas as pd

def eda_summary(stations):
    """
    Input: stations - list of Skyfield Satellite objects
    Output: df_meta - DataFrame with satellite info
            summary - dict with basic stats
    """
    data = {
        "Name": [sat.name for sat in stations],
        "Epoch": [sat.epoch.utc_datetime() for sat in stations],
        "Inclination": [sat.model.inclo for sat in stations],
        "Mean Motion": [sat.model.no_kozai for sat in stations]
    }
    df_meta = pd.DataFrame(data)
    summary = {
        "Total Satellites": len(df_meta),
        "Inclination Mean": df_meta["Inclination"].mean(),
        "Mean Motion Mean": df_meta["Mean Motion"].mean()
    }
    return df_meta, summary
